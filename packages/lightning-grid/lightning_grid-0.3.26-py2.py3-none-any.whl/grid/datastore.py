from dataclasses import dataclass
from dataclasses import field
from enum import Enum
import json
import logging
import math
import os
from pathlib import Path
import shutil
from threading import Lock
from typing import Callable, Dict, List
import uuid

from dataclasses_json import dataclass_json
from gql import Client
from gql import gql

from grid.tar import tar_and_split_directory
from grid.uploader import S3Uploader
from grid.uploader import UploadProgressCallback


class DatastoreUploadSteps(str, Enum):
    GET_PRESIGNED_URLS = "get_presigned_urls"
    COMPRESS_SOURCE_DIRECTORY = "compress_source_directory"
    UPLOAD_PARTS = "upload_parts"
    MARK_UPLOAD_COMPLETE = "mark_upload_complete"


@dataclass_json
@dataclass
class DatastoreUploadSession(UploadProgressCallback):
    """
    This class handles uploading datastore

    Attributes
    ----------
    name: str
        Name of the datastore
    source_dir: str
        Source directory to upload from
    credential_id: str
        Credential Id to use for uploading
    presigned_urls: Dict[int, str]
        Presigned urls retrieved from backend
    etags: Dict[int, str]
        Etags per part after uploading to cloud
    session_path: str
        Path to session files (data and state file)
    session_state_file: str
        Path to session state file
    """
    # Path storing datastore session and compresed data
    grid_datastores_path = '.grid/datastores'

    # Datastore upload fields
    name: str
    source_dir: str
    credential_id: str

    version: int = 1
    id: str = ""
    upload_id: str = ""
    original_size: int = 0
    part_count: int = 0

    # Session state
    session_id: str = ""
    session_path: str = ""
    session_state_file: str = ""
    last_completed_step: DatastoreUploadSteps = None

    presigned_urls: Dict[int, str] = field(default_factory=dict)
    etags: Dict[int, str] = field(default_factory=dict)

    def configure(self,
                  progress_callback: Callable,
                  client: Client,
                  session_id: str = ""):
        self.progress_callback = progress_callback
        self.client = client
        self.lock = Lock()
        self.logger = logging.getLogger("uploader.DatastoreUploadSession")

    @staticmethod
    def recover_sessions() -> List['DatastoreUploadSession']:
        """
        Recover all upload sessions that wasn't completed, so
        user can resume them.

        Returns
        -------
        List[DatastoreUploadSession]
            List of resumable sessions
        """
        logger = logging.getLogger("DatastoreUploadSession")
        sessions = []
        session_path = str(Path.home().joinpath(
            DatastoreUploadSession.grid_datastores_path))
        session_dirs = os.listdir(session_path)
        for session_dir in session_dirs:
            session_dir = os.path.join(session_path, session_dir)
            try:
                session = DatastoreUploadSession.recover(session_dir)
                last_completed_step = session.last_completed_step
                if last_completed_step in \
                    [None, DatastoreUploadSteps.COMPRESS_SOURCE_DIRECTORY]:
                    # We choose not to resume sessions that hasn't finished getting
                    # presigned_urls, since the datastore version is only determined
                    # when that's called, and we don't know what version we're going
                    # to be resuming.
                    raise ValueError("Session not yet finished compression")

                sessions.append(session)
            except ValueError as e:
                logger.warning(
                    f"Removing incomplete session {session_dir}, reason: {e}")
                shutil.rmtree(session_dir, ignore_errors=True)

        return sessions

    @staticmethod
    def recover(session_dir: str):
        """
        Recover session if sessions exists
        """
        session_state_file = os.path.join(session_dir, "session.json")
        if not os.path.exists(session_state_file):
            raise ValueError("Session state file does not exist")

        with open(session_state_file, "r") as f:
            content = json.load(f)
            session = DatastoreUploadSession.from_dict(content)

        return session

    def _update_progress(self, text: str):
        """
        Update current progress

        Parameters
        ----------
        text: str
            Latest progress text
        """
        self.progress_callback(text)

    def _get_presigned_urls(self):
        """Gets presigned urls from backend"""
        self._update_progress("Requesting presigned URLs from Grid...")

        query = gql("""
        query GetPresignedUrls (
            $credentialId: String!,
            $datastoreName: String!,
            $count: Int!
        ) {
            getPresignedUrls (
                credentialId: $credentialId,
                datastoreName: $datastoreName,
                count: $count
            ) {
                datastoreId
                datastoreVersion
                uploadId
                presignedUrls {
                    url
                    part
                }
            }
        }
        """)
        params = {
            'credentialId': self.credential_id,
            'datastoreName': self.name,
            'count': self.part_count
        }

        result = self.client.execute(query, variable_values=params)

        result = result['getPresignedUrls']
        self.version = result['datastoreVersion']
        presigned_urls = result['presignedUrls']
        self.upload_id = result['uploadId']
        self.id = result['datastoreId']
        presigned_map = {}
        for url in presigned_urls:
            presigned_map[int(url['part'])] = url['url']

        self.presigned_urls = presigned_map

    @property
    def target_file(self) -> str:
        """Get target compressed data file"""
        return os.path.join(self.session_path, "data.tar.gz")

    def _compress_source_directory(self):
        self._update_progress(f"Compressing datastore {self.name}...")
        tar_results = tar_and_split_directory(
            source_dir=self.source_dir, target_file_prefix=self.target_file)
        self.original_size, self.part_count = tar_results

    def _create_uploader(self, presigned_urls: Dict[int, str]):
        return S3Uploader(source_file_prefix=self.target_file,
                          presigned_urls=presigned_urls,
                          progress_callback=self)

    def _upload_parts(self):
        self._update_progress(
            f"Uploading datastore {self.name} (v{self.version}) datastore" +
            " to S3...")

        # Skip uploading parts that is already uploaded.
        # This can happen if we resume an upload session.
        unuploaded_presigned_urls = {}
        for part, url in self.presigned_urls.items():
            if part not in self.etags:
                unuploaded_presigned_urls[part] = url

        uploader = self._create_uploader(
            presigned_urls=unuploaded_presigned_urls)
        uploader.upload()

    def _mark_upload_complete(self):
        self._update_progress("Completing datastore uploads with Grid...")
        mutation = gql("""
        mutation (
            $name: String!
            $version: Int!
            $uploadId: String!
            $credentialId: String!
            $parts: JSONString!
            $size: Int!
            ) {
            uploadDatastore (
                properties: {
                        name: $name
                        version: $version
                        uploadId: $uploadId
                        credentialId: $credentialId
                        parts: $parts,
                        size: $size
                    }
            ) {
            success
            message
            }
        }
        """)

        params = {
            'name': self.name,
            'version': self.version,
            'uploadId': self.upload_id,
            'credentialId': self.credential_id,
            'parts': json.dumps(self.etags),
            'size': math.ceil(self.original_size / (1024**2))
        }

        result = self.client.execute(mutation, variable_values=params)
        success = result['uploadDatastore']['success']
        message = result['uploadDatastore']['message']
        if not success:
            raise ValueError(f"Unable to complete datastore upload: {message}")

    def _create_session_file(self, session_id: str):
        """
        Create session state file so we can resume upload progress.
        """
        self.session_path = os.path.join(self.grid_datastores_path, session_id)
        self.session_path = str(Path.home().joinpath(self.session_path))
        Path.home().joinpath(self.session_path).mkdir(parents=True,
                                                      exist_ok=True)
        self.session_file = os.path.join(self.session_path, "session.json")

    @property
    def session_name(self) -> str:
        return f"{self.name}-v{self.version}"

    def upload(self):
        """
        Upload completes the full datastore upload operation,
        and also records the progress of the upload, so
        it can be resumed later.
        """
        if self.session_id == "":
            self.session_id = str(uuid.uuid4())

        self._create_session_file(self.session_id)

        steps = [(self._compress_source_directory,
                  DatastoreUploadSteps.COMPRESS_SOURCE_DIRECTORY),
                 (self._get_presigned_urls,
                  DatastoreUploadSteps.GET_PRESIGNED_URLS),
                 (self._upload_parts, DatastoreUploadSteps.UPLOAD_PARTS),
                 (self._mark_upload_complete,
                  DatastoreUploadSteps.MARK_UPLOAD_COMPLETE)]

        current_step = 0
        if self.last_completed_step:
            for i, step in enumerate(steps):
                if step[1] == self.last_completed_step:
                    current_step = i + 1
                    break

            if current_step == 0:
                raise ValueError(f"Unsupported upload step: " +
                                 self.last_completed_step)

        try:
            while current_step < len(steps):
                func, step = steps[current_step]
                func()
                self.last_completed_step = step
                self.__write_session()
                current_step += 1

            self._remove_session()

        except (Exception, KeyboardInterrupt) as e:
            message = f"""
            Whoops, your datastore creation failed!

            To resume, run:

            grid datastores resume {self.session_name}
            """
            self.logger.error(message)
            raise e

    def upload_part_completed(self, part: int, etag: str):
        """
        Mark part uploaded

        Parameters
        ----------
        part: int
            Part number
        etag: str
            ETag returned
        """
        self.logger.debug(f"Part {part} finished uploading")
        with self.lock:
            self.etags[part] = etag
            self.__write_session()

    def __write_session(self):
        """
        Writes the session state into session file
        """
        with open(self.session_file, "w") as f:
            json.dump(self.to_dict(), f)

    def _remove_session(self):
        shutil.rmtree(self.session_path, ignore_errors=True)
