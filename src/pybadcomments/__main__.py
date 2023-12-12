# __main__.py

import logging

import click

from pybadcomments import __version__ as prog_version
from pybadcomments.files import FileDiscovery, load_config

from .options import GlobalOptions

Discovery = FileDiscovery

EXCLUDE_OPTION = {
    "multiple": True,
    "help": "A directory to be excluded. e.g. -x tests/ --exclude samples/big_samples/",
}
VERBOSE_OPTION = {
    "is_flag": True,
    "default": False,
    "help": "Print more logging messages.",
}


logger = logging.getLogger("pybadcomments")


@click.command()
@click.argument("strings", nargs=-1)
@click.argument("dir", default=".", nargs=1)
@click.option("-x", "--exclude", **EXCLUDE_OPTION)
@click.option("-v", "--verbose", **VERBOSE_OPTION)
@click.version_option(prog_version)
def entrypoint(
    exclude: tuple[str, ...], verbose: bool, strings: tuple[str, ...], dir: tuple[str]
) -> None:
    """A linter that searches for banned words in Python files."""
    # pylint: disable=W0622
    # pylint: disable=W0613
    print(f"got words: {strings=}")
    print(f"got dir: {dir=}")
    print(f"got exclude: {exclude=}")

    pyproj_config = load_config(dir)
    if pyproj_config:
        global_options = GlobalOptions.create_from_pyproj_config(pyproj_config)
        global_options.set_with_options(exclude_paths=exclude)
    else:
        global_options = GlobalOptions(exclude_paths=exclude)

    if verbose:
        logger.setLevel(logging.DEBUG)

    strings += tuple(pyproj_config.get("words", ()))
    print(global_options)
    print(verbose)
    print(strings)

    # Get files/filepaths to parse
    found_files = list(Discovery.parse_python_files(dir))

    # Parse files with runner, where runner will apply given
    # analysers to each line as it's parsed (using generators)

    # Gather report and print out
    # Exit


def main() -> None:
    # pylint: disable=E1120
    entrypoint(prog_name="pybadcomments")


if __name__ == "__main__":
    main()
