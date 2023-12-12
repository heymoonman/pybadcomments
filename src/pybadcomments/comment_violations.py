# comment_violations.py

from dataclasses import dataclass


@dataclass(frozen=True)
class CommentViolation:
    """Holds information regarding a violation found in a comment."""

    filename: str
    lineno: str
    violating_phrase: str
