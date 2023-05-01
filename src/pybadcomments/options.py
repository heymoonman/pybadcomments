# options.py

from __future__ import annotations

from typing import Iterable

from .config import PyProjectConfig

EXCLUDE_DEFAULT = ()


class GlobalOptions:
    exclude_paths: Iterable[str]

    def __init__(self, exclude_paths: Iterable[str]) -> None:
        self.exclude_paths = exclude_paths

    @classmethod
    def create_from_pyproj_config(cls, config: PyProjectConfig) -> GlobalOptions:
        exclude = config.get("exclude", EXCLUDE_DEFAULT)

        return cls(exclude_paths=exclude)

    def set_with_options(self, *, exclude_paths: Iterable[str] = None) -> None:
        if exclude_paths:
            self.exclude_paths = exclude_paths

    def should_skip_path(self, path: str) -> bool:
        return any(excluded_path in path for excluded_path in self.exclude_paths)
