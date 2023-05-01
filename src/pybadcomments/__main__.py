# __main__.py

import click

EXCLUDE_OPTION = {
    "multiple": True,
    "help": "A directory to be excluded. e.g. -x tests --exclude samples/",
}


@click.command()
@click.argument("words", nargs=-1)
@click.argument("dir", default=".", nargs=1)
@click.option("-x", "--exclude", **EXCLUDE_OPTION)
def entrypoint(
    words: tuple[str, ...], dir: tuple[str], exclude: tuple[str, ...]
) -> None:
    """A linter that searches for banned words in Python files."""
    # pylint: disable=W0622
    # pylint: disable=W0613
    print(words)
    print(dir)
    print(exclude)


def main() -> None:
    # pylint: disable=E1120
    entrypoint()


if __name__ == "__main__":
    main()
