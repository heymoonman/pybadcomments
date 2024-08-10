# analysers/base.py

from abc import ABC, abstractmethod
from pathlib import Path
from tokenize import TokenInfo

from pybadcomments.comment_violations import CommentViolation
from pybadcomments.options import GlobalOptions


class BaseTokenInfoAnalyser(ABC):
    def __init__(self, settings: GlobalOptions = GlobalOptions()) -> None:
        self.violations: list[CommentViolation] = []
        self._settings = settings

    @abstractmethod
    def analyse(
        self, to_analyse: TokenInfo, file_path: Path | str | None = None
    ) -> None:
        ...

    def reset_violations(self) -> None:
        self.violations = []
