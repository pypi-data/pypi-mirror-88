import os
import tarfile
import tempfile
import unittest

from grid.tar import get_dir_size_and_count
from grid.tar import tar_and_split_directory


class TarTestCase(unittest.TestCase):
    """
    Test tar
    """
    @staticmethod
    def test_get_dir_size_and_count():
        sizes = [1024 * 512, 1024 * 1024 * 5]

        for size in sizes:
            with tempfile.TemporaryDirectory() as temp_dir:
                data = os.urandom(size)
                with open(os.path.join(temp_dir, "a"), "wb") as f:
                    f.write(data)
                with open(os.path.join(temp_dir, "b"), "wb") as f:
                    f.write(data)
                assert get_dir_size_and_count(temp_dir, "a") == (size, 1)

    @staticmethod
    def test_tar_directory():
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = os.path.join(temp_dir, "source")
            inner_dir = os.path.join(source_dir, "dir")
            os.makedirs(inner_dir)
            with open(os.path.join(source_dir, "f1"), 'w') as f:
                f.write("f1")

            with open(os.path.join(inner_dir, "f2"), 'w') as f:
                f.write("f2")

            target_file = os.path.join(temp_dir, "target.tar.gz")
            tar_and_split_directory(source_dir=source_dir,
                                    target_file_prefix=target_file)

            verify_dir = os.path.join(temp_dir, "verify")
            os.makedirs(verify_dir)
            with tarfile.open(target_file + ".aa") as target_tar:
                target_tar.extractall(verify_dir)

            assert os.path.exists(os.path.join(verify_dir, "f1"))
            assert os.path.exists(os.path.join(verify_dir, "dir", "f2"))
