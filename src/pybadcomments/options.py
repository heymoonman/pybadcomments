# options.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .config import PyProjectConfig


@dataclass(frozen=True)
class GlobalOptions:
    banned_strings: Iterable[str] = field(default_factory=tuple)
    exclude_paths: Iterable[str] = field(default_factory=tuple)
    verbose: bool = False

    @classmethod
    def create_from_pyproj_config(
        cls,
        config: PyProjectConfig,
        banned_strings: Iterable[str] = None,
        exclude_paths: Iterable[str] = None,
        verbose: bool = False,
    ) -> GlobalOptions:
        if not banned_strings:
            banned_strings = config.get("strings", [])
        if not exclude_paths:
            exclude_paths = config.get("exclude", [])
        if not verbose:
            verbose = config.get("verbose", False)

        return cls(
            banned_strings=banned_strings, exclude_paths=exclude_paths, verbose=verbose
        )

    def should_skip_path(self, path: str) -> bool:
        return any(excluded_path in path for excluded_path in self.exclude_paths)
