# interfaces.py

import sys
from enum import IntEnum


class ExitCodes(IntEnum):
    SUCCESS = 0
    LINT_BROKEN = 1
    UNPROCESSED_FILE = 2
    RUNTIME_ISSUES = 100


class CliInterface:
    def __init__(self) -> None:
        ...

    def _exit(self) -> None:
        exit_code = ExitCodes.SUCCESS

        # Checks for other exit scenarios

        sys.exit(exit_code)

    def report_and_exit(self) -> None:
        ...
