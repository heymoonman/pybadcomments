# __main__.py

import logging
from pathlib import Path

import click

from pybadcomments import __version__ as prog_version
from pybadcomments.analysers import HashCommentAnalyser
from pybadcomments.files import FileDiscovery, load_config
from pybadcomments.options import GlobalOptions
from pybadcomments.processors import TokenizingProcessor
from pybadcomments.runner import Runner

discovery = FileDiscovery()

EXCLUDE_OPTION = {
    "multiple": True,
    "help": "A directory to be excluded. e.g. -x tests/ --exclude samples/big_samples/",
}
VERBOSE_OPTION = {
    "is_flag": True,
    "default": False,
    "help": "Print more logging messages.",
}


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

    if dir == ".":
        root_dir = Path.cwd()
    else:
        root_dir = Path(dir)

    print(f"got words: {strings=}")
    print(f"got dir: {root_dir=}")
    print(f"got exclude: {exclude=}")

    pyproj_config = load_config(root_dir)
    if pyproj_config:
        global_options = GlobalOptions.create_from_pyproj_config(
            pyproj_config,
            banned_strings=strings,
            exclude_paths=exclude,
            verbose=verbose,
        )
    else:
        global_options = GlobalOptions(
            banned_strings=strings, exclude_paths=exclude, verbose=verbose
        )

    if global_options.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # print(global_options)
    # print(global_options.verbose)
    # print(global_options.banned_strings)
    # print(global_options.exclude_paths)

    # Get files/filepaths to parse
    discovery.parse_files_from_file_path(root_dir)

    # Setup analysers to use
    hash_analyser = HashCommentAnalyser(global_options)

    # Setup processors to use
    token_processor = TokenizingProcessor([hash_analyser])

    # Parse files with runner, which will process the files
    runner = Runner()
    runner.analyse_files(discovery.files, (token_processor,))
    results = runner.create_analysis_results(verbose)

    # Gather report and print out
    # Exit
    if results.violation_count > 0:
        print(str(results))
        exit(1)
    exit(0)


def main() -> None:
    # pylint: disable=E1120
    entrypoint(prog_name="pybadcomments")


if __name__ == "__main__":
    main()
