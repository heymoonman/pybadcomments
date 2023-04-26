# __main__.py

import click

WORDS_TO_IGNORE_OPTION = {
    "multiple": True,
    "help": """A list of words to be ignored. e.g. -i ["fudge", "workaround"]
    -i ["terrible"]""",
}


@click.command()
@click.argument("dir", default=".", nargs=1)
@click.option("-i", "--include", **WORDS_TO_IGNORE_OPTION)
def entrypoint(dir: tuple[str], include: tuple[str, ...]) -> None:
    # pylint: disable=W0622
    # pylint: disable=W0613
    ...


def main() -> None:
    # pylint: disable=E1120
    entrypoint()


if __name__ == "__main__":
    main()
