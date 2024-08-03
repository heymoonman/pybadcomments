# config.py

from typing import TypedDict


class PyProjectConfig(TypedDict):
    """
    The expected configuration for the application:
        exclude: A list of paths to be excluded from the file discovery.
        verbose: How verbose the printed results and logging should be.
        strings: The list of banned strings to search for and raise violations on.
    """

    exclude: list[str]
    verbose: bool
    strings: list[str]
