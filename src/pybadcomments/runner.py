# runner.py

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Iterable

from src.pybadcomments.analysers import BaseTokenInfoAnalyser
from src.pybadcomments.comment_violations import CommentViolation
from src.pybadcomments.processors import Processor


@dataclass(frozen=True)
class AnalysisResults:
    violations: Iterable[CommentViolation]
    analysed_files: int
    excluded_files: int
    verbose: bool = False

    def __str__(self) -> str:
        output = ""
        if not self.violations:
            return output

        for violation in self.violations:
            output += f"\n{str(violation)}\n"

        return output

    @property
    def violation_count(self) -> int:
        return len(self.violations)

    def analysis_results(self) -> str:
        return self.__str__()


class Runner:
    """Runners will take an iterable of file paths and an iterable of loaded processor
    objects to process the files with, generating any comment violations and storing
    them ready to be reported.
    """

    def __init__(self) -> None:
        self.comment_violations: list[CommentViolation] = []
        self.analysed_files = 0
        self.excluded_files = 0

    def _check_for_violations(self, analysers: Iterable[BaseTokenInfoAnalyser]):
        for analyser in analysers:
            if analyser.violations:
                self.comment_violations.extend(analyser.violations)

    def analyse_files(
        self,
        file_paths: Iterable[Path],
        processors: Iterable[Processor],
    ):
        for processor in processors:
            processor.batch_process_files(file_paths)
            if processor.violations:
                self.comment_violations.extend(processor.comment_violations)

    def create_analysis_results(self, verbose: bool = False) -> AnalysisResults:
        return AnalysisResults(
            self.comment_violations, self.analysed_files, self.excluded_files, verbose
        )
