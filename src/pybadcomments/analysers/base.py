# analysers/base.py

from abc import ABC, abstractmethod
from typing import Any

from pybadcomments.options import GlobalOptions


class BaseAnalyser(ABC):
    def __init__(self, settings: GlobalOptions = None) -> None:
        self.violations = []
        self._settings = settings

    @abstractmethod
    def analyse(self, to_analyse: Any):
        ...
