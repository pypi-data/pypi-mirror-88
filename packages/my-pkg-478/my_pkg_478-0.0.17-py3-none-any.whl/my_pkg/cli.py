"""Console script for my-pkg."""

import sys
import click


@click.command()
def my_pkg(args=None):
    """Console script for my-pkg."""
    # fmt: off
    click.echo("Replace this message by putting your code into "
               "my_pkg.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    # fmt: on
    return 0


if __name__ == "__main__":
    sys.exit(my_pkg)  # pragma: no cover
