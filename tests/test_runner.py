# test_runner.py

from logging import getLogger

from src.pybadcomments.comment_violations import CommentViolation
from src.pybadcomments.runner import AnalysisResults, Runner

logger = getLogger(__name__)


def test_printing_results_does_not_throw_error():
    comment1 = CommentViolation("sample1.py", 5, 10, "The wind hates you", "hate")
    comment2 = CommentViolation("sample2.py", 62, 1, "Dumb code", "Dumb")

    results = AnalysisResults([comment1, comment2], 2, 0, False)
    logger.info(str(results))
