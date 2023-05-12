# parser.py

import re
import tokenize
from typing import Generator, Iterable, TextIO

from pybadcomments.comment_violations import CommentViolation


def _parse_tokens_from_file(
    tokens: Iterable[tokenize.TokenInfo],
) -> Generator[CommentViolation, None, None]:
    # pylint: disable=W0612
    for token in tokens:
        toktype, tokval, start, *_ = token
        if toktype == tokenize.COMMENT:
            if match := re.search("bruh", tokval):
                yield


def parse_comments_from_file(
    content: TextIO,
) -> Generator[CommentViolation, None, None]:
    tokens = tokenize.generate_tokens(content.readline)
    yield from _parse_tokens_from_file(tokens)


def parse_file(filename: str) -> tuple[CommentViolation]:
    with open(filename, "r", encoding="utf-8") as file:
        comments = list(parse_comments_from_file(file))

    return comments
