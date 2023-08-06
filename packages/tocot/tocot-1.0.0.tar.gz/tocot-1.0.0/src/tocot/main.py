"""main.

main is controller for cli.

"""
import typing

import click

from .toc_builder import TOCBuilder


def validate_level(ctx, param, value):
    """Validate level option.

    validate level option.
    level is greater than 0, and less than 6.

    """
    level = value

    if level <= 0:
        raise click.BadParameter("level must be greater than 0.")
    if level > 5:
        raise click.BadParameter("level must be less than 6")

    return level


@click.command()
@click.argument("in_file", type=click.File("r"))
@click.argument("out_file", type=click.File("w"))
@click.option("--level",
              "-l",
              callback=validate_level,
              default=2,
              show_default=True,
              type=int)
@click.option("--to_embed", "-e", default="[TOC]", show_default=True, type=str)
@click.option("--exclude_symbol",
              default="exclude-toc",
              show_default=True,
              type=str)
def cmd(in_file: typing.TextIO, out_file: typing.TextIO, level: int,
        to_embed: str, exclude_symbol: str) -> None:
    """Cmd.

    cmd is a controller.

    """
    builder = TOCBuilder(in_file, out_file, level, to_embed, exclude_symbol)
    builder.build()
    builder.write()


def main():
    """Vain.

    main is a entrypoint.

    """
    cmd()


if __name__ == "__main__":
    main()
