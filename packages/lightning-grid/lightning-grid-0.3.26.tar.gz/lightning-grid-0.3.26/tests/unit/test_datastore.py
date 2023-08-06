import json
import math
from typing import Any, Dict
import unittest

from _pytest.monkeypatch import MonkeyPatch

from grid.datastore import DatastoreUploadSession
import grid.datastore as datastore


class DatastoreTestCase(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        datastore.gql = lambda x: x

    @staticmethod
    def test_datastore_steps():
        session = DatastoreUploadSession(name="test",
                                         source_dir="test_dir",
                                         credential_id="cc-abcdef")

        progress_texts = []

        def progress_callback(text):
            progress_texts.append(text)

        class MockS3Uploader:
            def __init__(self, session):
                self.session = session

            def upload(self):
                self.session.upload_part_completed(1, "etag1")
                self.session.upload_part_completed(2, "etag2")

        class MockClient:
            def execute(self, query, variable_values):
                if "GetPresignedUrls" in query:
                    assert variable_values == {
                        'credentialId': 'cc-abcdef',
                        'datastoreName': 'test',
                        'count': 50
                    }

                    return {
                        'getPresignedUrls': {
                            'datastoreVersion': 1,
                            'presignedUrls': [],
                            'uploadId': "upload1",
                            'datastoreId': "abcde"
                        }
                    }
                if "uploadDatastore" in query:
                    assert variable_values == {
                        'name': 'test',
                        'version': 1,
                        'uploadId': 'upload1',
                        'credentialId': 'cc-abcdef',
                        'parts': json.dumps({
                            1: "etag1",
                            2: "etag2"
                        }),
                        'size': math.ceil((1024 * 1000 * 1000) / (1024**2))
                    }

                    return {
                        'uploadDatastore': {
                            'success': True,
                            'message': ''
                        }
                    }

                raise ValueError(f"Unexpected query {query}")

        client = MockClient()
        session.configure(progress_callback=progress_callback, client=client)

        m = MonkeyPatch()

        def tar_and_split_directory(**kwargs):
            return 1024 * 1000 * 1000, 50

        def create_uploader(presigned_urls):
            return MockS3Uploader(session)

        m.setattr('grid.datastore.tar_and_split_directory',
                  tar_and_split_directory)
        m.setattr(session, '_create_uploader', create_uploader)

        session.upload()
        assert len(progress_texts) == 4
