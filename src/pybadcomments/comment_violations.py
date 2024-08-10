# comment_violations.py

from dataclasses import dataclass
from pathlib import Path
from typing import Union


@dataclass(frozen=True)
class CommentViolation:
    """Holds information regarding a violation found in a comment."""

    filename: Union[Path, str]
    lineno: int
    columnno: int
    full_comment: str
    violating_phrase: str

    def __str__(self) -> str:
        return f"""{self.filename}
{self.lineno}:{self.columnno} - Found violating string match
Violating string - "{self.violating_phrase}"
-> {self.full_comment} <-"""


@dataclass(frozen=True)
class FileAnalysisResult:
    """Returned from analysing a file with an analyser, specifying if
    any violations have occurred and providing the violations"""

    violation_found: bool
    violations: list[CommentViolation]
