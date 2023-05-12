# discovery.py

from dataclasses import dataclass
from logging import getLogger
from os import listdir
from os.path import isdir, isfile, join
from pathlib import Path
from typing import Generator, Iterable, Sequence

import toml

from pybadcomments.config import PyProjectConfig

logger = getLogger(__name__)


def is_python_file(filename: str) -> bool:
    return isfile(filename) and filename.endswith(".py")


def find_files_in_dir(dir_: str) -> Generator[str, None, None]:
    files = listdir(dir_)
    for file_path in files:
        full_path = join(dir_, file_path)
        if isdir(full_path):
            yield from find_files_in_dir(full_path)
        elif is_python_file(full_path):
            yield full_path


@dataclass(frozen=True)
class FileParseFailed:
    filename: str
    reason: str
    exception: Exception


class FileDiscovery:
    def __init__(self) -> None:
        self.failures: list[FileParseFailed] = []

    @property
    def had_issues(self) -> bool:
        return len(self.failures) > 0

    def _parse_files_from_file_path(self, file_path: str) -> Generator[str, None, None]:
        # pylint: disable=W0718
        files = []
        if is_python_file(file_path):
            files.append(file_path)
        elif isdir(file_path):
            files = list(find_files_in_dir(file_path))

        for filename in files:
            try:
                pass
            except Exception as ex:
                logger.exception("Failed to parse file: %s", filename)
                self.failures.append(FileParseFailed(filename, str(ex), ex))

    def parse_python_files(self, files: Iterable[str]):
        # pylint: disable=E1133
        for file in files:
            yield from self._parse_files_from_file_path(file)


def find_project_root(srcs: Sequence[str]) -> Path:
    """Return a directory containing .git, .hg, or pyproject.toml.

    That directory will be a common parent of all files and directories
    passed in `srcs`.

    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.
    """
    if not srcs:
        srcs = [str(Path.cwd().resolve())]

    path_srcs = [Path(Path.cwd(), src).resolve() for src in srcs]

    # A list of lists of parents for each 'src'. 'src' is included as a
    # "parent" of itself if it is a directory
    src_parents = [
        list(path.parents) + ([path] if path.is_dir() else []) for path in path_srcs
    ]

    common_base = max(
        set.intersection(*(set(parents) for parents in src_parents)),
        key=lambda path: path.parts,
    )

    for directory in (common_base, *common_base.parents):
        if (directory / ".git").exists():
            return directory

        if (directory / ".hg").is_dir():
            return directory

        if (directory / "pyproject.toml").is_file():
            return directory

    return directory


def find_pyproject_toml(path_search_start: Sequence[str]) -> str | None:
    """Find the absolute filepath to a pyproject.toml if it exists"""
    path_project_root = find_project_root(path_search_start)
    path_pyproject_toml = path_project_root / "pyproject.toml"

    if path_pyproject_toml.is_file():
        return str(path_pyproject_toml)

    return None


def load_config(dir: Sequence[str]) -> PyProjectConfig | None:
    # pylint: disable=W0622
    toml_file = find_pyproject_toml(dir)

    if toml_file:
        config = toml.load(toml_file)
        return config.get("tool", {}).get("pybadcomments", {})

    return None
