"""
Create tar file from folder
"""

import math
import os
import subprocess
from typing import Optional, Tuple


def get_dir_size_and_count(source_dir: str,
                           prefix: Optional[str] = None) -> Tuple[int, int]:
    """
    Get size and file count of a directory

    Parameters
    ----------
    source_dir: str
        Directory path

    Returns
    -------
    Tuple[int, int]
        Size in megabytes and file count
    """
    size = 0
    count = 0
    for root, _, files in os.walk(source_dir, topdown=True):
        for f in files:
            if prefix and not f.startswith(prefix):
                continue

            full_path = os.path.join(root, f)
            size += os.path.getsize(full_path)
            count += 1

    return (size, count)


def tar_and_split_directory(source_dir: str,
                            target_file_prefix: str,
                            minimum_split_size: int = 1024 * 1000 * 10) \
                            -> Tuple[int, int]:
    """
    Create tar from directory using `tar`, and split the files
    into specific chunks

    Parameters
    ----------
    source_dir: str
        Source directory
    target_file_prefix: str
        Target tar file
    split_size: str
        Split file size

    Returns
    -------
    Tuple[int, int]
        Before compression data size and part count
    """
    # Unix split max only supports up to 676 parts, so we have to cut
    # the file up to stay below this count.
    max_split_count = float(26**2 - 1)
    size, _ = get_dir_size_and_count(source_dir)
    split_size = minimum_split_size
    split_count = math.ceil(size / split_size)
    if split_count > max_split_count:
        split_size = math.ceil(size / max_split_count)

    command = f"tar -C {source_dir} -zcv ./ | split -b {split_size} - " \
              f"{target_file_prefix}."
    subprocess.check_call(command,
                          stderr=subprocess.DEVNULL,
                          shell=True,
                          env={"GZIP": "-9"})

    target_dir = os.path.dirname(target_file_prefix)
    basename = os.path.basename(target_file_prefix)
    _, part_count = get_dir_size_and_count(source_dir=target_dir,
                                           prefix=basename)
    return size, part_count
