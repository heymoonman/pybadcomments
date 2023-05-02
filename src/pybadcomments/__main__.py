# __main__.py

import logging

import click

from pybadcomments import __version__ as prog_version
from pybadcomments.files import load_config

from .options import GlobalOptions

EXCLUDE_OPTION = {
    "multiple": True,
    "help": "A directory to be excluded. e.g. -x tests --exclude samples/",
}
VERBOSE_OPTION = {
    "is_flag": True,
    "default": False,
    "help": "Print more logging messages.",
}


logger = logging.getLogger("pybadcomments")


@click.command()
@click.argument("words", nargs=-1)
@click.argument("dir", default=".", nargs=1)
@click.option("-x", "--exclude", **EXCLUDE_OPTION)
@click.option("-v", "--verbose", **VERBOSE_OPTION)
@click.version_option(prog_version)
def entrypoint(
    exclude: tuple[str, ...], verbose: bool, words: tuple[str, ...], dir: tuple[str]
) -> None:
    """A linter that searches for banned words in Python files."""
    # pylint: disable=W0622
    # pylint: disable=W0613
    print(words)
    print(dir)
    print(exclude)

    pyproj_config = load_config(dir)
    if pyproj_config:
        global_options = GlobalOptions.create_from_pyproj_config(pyproj_config)
        global_options.set_with_options(exclude_paths=exclude)
    else:
        global_options = GlobalOptions(exclude_paths=exclude)

    if verbose:
        logger.setLevel(logging.DEBUG)

    print(global_options)
    print(verbose)


def main() -> None:
    # pylint: disable=E1120
    entrypoint(prog_name="pybadcomments")


if __name__ == "__main__":
    main()
