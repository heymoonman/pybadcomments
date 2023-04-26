# config.py

from typing import TypedDict


class PyProjectConfig(TypedDict):
    """
    The expected configuration for the application:
        include: A list of words and phrases that will be searched for and warned on
    """

    include: list[str]
