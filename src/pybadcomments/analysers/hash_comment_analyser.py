# hash_comment_analyser.py

from tokenize import COMMENT, TokenInfo

from src.pybadcomments.comment_violations import CommentViolation

from .base import BaseTokenInfoAnalyser


class HashCommentAnalyser(BaseTokenInfoAnalyser):
    def analyse(self, to_analyse: TokenInfo, filename: str = "UNKNOWN"):
        if not to_analyse[0] == COMMENT:
            return
        for banned_string in self._settings.banned_strings:
            if banned_string in to_analyse[1]:
                new_violation = CommentViolation(
                    filename,
                    to_analyse[2][0],
                    to_analyse[2][1],
                    to_analyse[1],
                    banned_string,
                )
                self.violations.append(new_violation)
