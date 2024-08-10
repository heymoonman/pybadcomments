# test_hash_comment_analyser.py

import tokenize
from io import BytesIO
from logging import getLogger

from src.pybadcomments.analysers import HashCommentAnalyser
from src.pybadcomments.options import GlobalOptions

logger = getLogger(__name__)


def test_hash_comment_single_word_violation():
    banned_word = "squid"
    options = GlobalOptions(banned_strings=[banned_word])
    test_file = """
from typing import Any

def dummy_func() -> Any:
    # we can do some squid games in here
    a = 1
    b = 2
    # wow huh squids
    c = a * b
    return c
    """
    logger.info(BytesIO(test_file.encode("utf-8")).readline)
    tokens = tokenize.tokenize(BytesIO(test_file.encode("utf-8")).readline)
    analyser = HashCommentAnalyser(options)
    for token in tokens:
        analyser.analyse(token)
    assert len(analyser.violations) == 2  # currently accepting an exact-match method


def test_banned_phrase_violation():
    banned_phrase = "rolling in the deep"
    options = GlobalOptions(banned_strings=[banned_phrase])
    sample = """
from typing import Any

def dummy_func() -> Any:
    # we can be rolling in the deep
    a = 2
    return a
"""
    tokens = tokenize.tokenize(BytesIO(sample.encode("utf-8")).readline)
    analyser = HashCommentAnalyser(options)
    for token in tokens:
        analyser.analyse(token)
    assert len(analyser.violations) == 1
