# discovery.py

import os
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Sequence

import toml

from pybadcomments.config import PyProjectConfig

logger = getLogger(__name__)

AVOID_DIRECTORIES_IF_CONTAINS = {
    "pyvenv.cfg",
}


def is_python_file(filename: str) -> bool:
    return os.path.isfile(filename) and filename.endswith(".py")


def is_allowed_directory(dir_path: str) -> bool:
    if dir_path.startswith("."):
        return False
    if any(file in AVOID_DIRECTORIES_IF_CONTAINS for file in os.listdir(dir_path)):
        return False
    return True


@dataclass(frozen=True)
class FileParseFailed:
    filename: str
    exception: Exception


class FileDiscovery:
    def __init__(self) -> None:
        self.failures: list[FileParseFailed] = []
        self.files: list[Path] = []

    def __str__(self) -> str:
        return f"FileDiscovery - Files: {self.files} - Failures: {self.failures}"

    @property
    def had_issues(self) -> bool:
        return len(self.failures) > 0

    def parse_files_from_file_path(self, file_path: str | Path) -> list[str]:
        # pylint: disable=W0718

        def rec_func(file_path: str):
            try:
                if is_python_file(file_path):
                    self.files.append(Path(file_path))
                elif os.path.isdir(file_path):
                    new_file_paths = os.listdir(file_path)
                    for fp in new_file_paths:
                        if os.path.isdir(fp) and not is_allowed_directory(fp):
                            continue
                        self.parse_files_from_file_path(os.path.join(file_path, fp))
            except Exception as exc:
                logger.warning("Failed parsing file path %s", file_path)
                print(exc)
                self.failures.append(FileParseFailed(filename=file_path, exception=exc))

        rec_func(file_path)


def find_project_root(srcs: Sequence[str]) -> Path:
    """Return a directory containing .git, .hg, or pyproject.toml.

    That directory will be a common parent of all files and directories
    passed in `srcs`.

    If no directory in the tree contains a marker that would specify it's the
    project root, the current working directory is returned.
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
