import os
import tempfile
from grid.uploader import S3Uploader
from grid.uploader import UploadProgressCallback


def test_alphabet_encode():
    tests = {1: "aa", 2: "ab", 26: "az", 26**2: "yz"}
    for number, expected in tests.items():
        assert S3Uploader.alphabet_encode(number) == expected


def test_s3_uploader():
    with tempfile.TemporaryDirectory() as tmpdir:
        data = {
            "aa": os.urandom(256),
            "ab": os.urandom(256),
            "ac": os.urandom(256),
            "ad": os.urandom(256)
        }
        for k, d in data.items():
            with open(os.path.join(tmpdir, f"data.{k}"), "wb") as f:
                f.write(d)

        urls = {
            1: "http://grid.ai/1",
            2: "http://grid.ai/2",
            3: "http://grid.ai/3",
            4: "http://grid.ai/4"
        }

        reverse_keys = {"aa": 1, "ab": 2, "ac": 3, "ad": 4}

        def mock_upload_data(url, part_file, _):
            part_data = part_file.read()
            found_key = None
            for k, d in data.items():
                if part_data == d:
                    found_key = k
                    break

            assert found_key
            part = reverse_keys[found_key]
            assert urls[part] == url
            return str(part)

        class MockProgressUpdater(UploadProgressCallback):
            def __init__(self):
                self.etags = {}

            def upload_part_completed(self, part: int, etag: str):
                self.etags[part] = etag

        updater = MockProgressUpdater()
        uploader = S3Uploader(source_file_prefix=os.path.join(tmpdir, "data"),
                              presigned_urls=urls,
                              progress_callback=updater)

        uploader.upload_s3_data = mock_upload_data

        uploader.upload()
        assert updater.etags == {1: "1", 2: "2", 3: "3", 4: "4"}
