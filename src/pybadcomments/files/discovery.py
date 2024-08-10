# discovery.py

import os
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from typing import Union

import toml

from src.pybadcomments.config import PyProjectConfig

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

    def parse_files_from_file_path(self, file_path: Union[str, Path]) -> list[str]:
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


def find_pyproject_toml(path_project_root: Path) -> Union[str, None]:
    """Find the absolute filepath to a pyproject.toml if it exists"""
    path_pyproject_toml = path_project_root / "pyproject.toml"

    if path_pyproject_toml.is_file():
        return str(path_pyproject_toml)

    return None


def load_config(project_root: Path) -> Union[PyProjectConfig, None]:
    # pylint: disable=W0622
    toml_file = find_pyproject_toml(project_root)

    if toml_file is not None:
        config = toml.load(toml_file)
        return config.get("tool", {}).get("pybadcomments", {})

    return None
