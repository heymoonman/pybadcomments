# config.py

from typing import TypedDict


class PyProjectConfig(TypedDict):
    """
    The expected configuration for the application:
        exclude: A list of paths to be excluded from the file discovery.
    """

    exclude: list[str]
