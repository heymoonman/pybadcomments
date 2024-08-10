# processors.py

import io
from abc import abstractmethod
from logging import getLogger
from pathlib import Path
from tokenize import TokenInfo, tokenize
from typing import Generator, Iterable, Union

from src.pybadcomments.analysers import BaseTokenInfoAnalyser
from src.pybadcomments.comment_violations import CommentViolation, FileAnalysisResult

logger = getLogger(__name__)


class Processor:
    def __init__(
        self, analysers: Union[list[BaseTokenInfoAnalyser], None] = None
    ) -> None:
        if analysers is None:
            analysers = []
        self.analysers = analysers
        self.comment_violations: list[CommentViolation] = []

    @property
    def violations(self) -> bool:
        if self.comment_violations:
            return True

    @abstractmethod
    def process_files(self, files: Iterable[Path]) -> None:
        ...

    @abstractmethod
    def batch_process_files(self, files: Iterable[Path]) -> None:
        ...


class TokenizingProcessor(Processor):
    def add_analyser(self, analyser: BaseTokenInfoAnalyser) -> None:
        self.analysers.append(analyser)

    def _parse_file(self, file: Path) -> Generator[TokenInfo, None, None]:
        # print(f"parsing file {file}")
        with open(file, "rb") as fp:
            contents = io.BytesIO(fp.read())
        tokens = tokenize(contents.readline)
        for token in tokens:
            yield token

    def _analyse_token_info(
        self, info: TokenInfo, file_path: Union[Path, str]
    ) -> FileAnalysisResult:
        violations = []
        for analyser in self.analysers:
            analyser.analyse(info, file_path)
            if analyser.violations:
                violations.extend(analyser.violations)
                analyser.reset_violations()
        if violations:
            return FileAnalysisResult(violation_found=True, violations=violations)
        return FileAnalysisResult(violation_found=False, violations=())

    def process_file(self, file: Path) -> None:
        for token in self._parse_file(file):
            analysis_result = self._analyse_token_info(token, file)
            if analysis_result.violation_found:
                self.comment_violations.extend(analysis_result.violations)

    def batch_process_files(self, files: Iterable[Path]) -> None:
        for file in files:
            self.process_file(file)
