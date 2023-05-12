# comment_violations.py

from dataclasses import dataclass


@dataclass(frozen=True)
class CommentViolation:
    def __init__(self, lineno: int, violating_phrase: str) -> None:
        self.lineno = lineno
        self.violating_phrase = violating_phrase
