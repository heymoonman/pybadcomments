# conftest.py

from pathlib import Path

from pytest import fixture


@fixture
def complaint_file_path() -> Path:
    return Path.cwd() / "tests" / "samples" / "complaint.py"


@fixture
def fudge_file_path() -> Path:
    return Path.cwd() / "tests" / "samples" / "fudge.py"


@fixture
def sample_violating_string_code() -> tuple[str, list[str]]:
    sample = """import os

def func(a: int) -> int:
    # this is a fudge
    b = a * 2
    return b

"""
    banned_strings = ["fudge"]
    return (sample, banned_strings)
