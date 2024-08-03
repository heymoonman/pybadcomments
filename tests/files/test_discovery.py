# test_discovery.py

from logging import getLogger
from pathlib import Path

from src.pybadcomments.files.discovery import FileDiscovery

logger = getLogger(__name__)


def test_discovering_one_python_file(fs):
    fs.create_file("sample.py")

    discovery = FileDiscovery()
    discovery.parse_files_from_file_path(Path.cwd())
    assert len(discovery.files) == 1


def test_discovering_multiple_files_in_directories(fs):
    fs.create_file("sample1.py")
    fs.create_dir("/src")
    fs.create_dir("/src/tests")
    fs.create_file("/src/sample2.py")
    fs.create_file("/src/sample3.py")
    fs.create_file("/src/tests/sample4.py")

    discovery = FileDiscovery()
    discovery.parse_files_from_file_path(Path.cwd())
    assert len(discovery.files) == 4
