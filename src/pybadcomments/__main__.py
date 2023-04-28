# __main__.py

import click


@click.command()
@click.argument("words", nargs=-1)
@click.argument("dir", default=".", nargs=1)
def entrypoint(words: tuple[str, ...], dir: tuple[str]) -> None:
    """A linter that searches for banned words in Python files."""
    # pylint: disable=W0622
    # pylint: disable=W0613
    print(words)
    print(dir)


def main() -> None:
    # pylint: disable=E1120
    entrypoint()


if __name__ == "__main__":
    main()
