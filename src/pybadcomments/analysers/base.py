# analysers/base.py

from abc import ABC, abstractmethod
from pathlib import Path
from tokenize import TokenInfo
from typing import Union

from src.pybadcomments.comment_violations import CommentViolation
from src.pybadcomments.options import GlobalOptions


class BaseTokenInfoAnalyser(ABC):
    def __init__(self, settings: GlobalOptions = GlobalOptions()) -> None:
        self.violations: list[CommentViolation] = []
        self._settings = settings

    @abstractmethod
    def analyse(
        self, to_analyse: TokenInfo, file_path: Union[Path, str, None] = None
    ) -> None:
        ...

    def reset_violations(self) -> None:
        self.violations = []
