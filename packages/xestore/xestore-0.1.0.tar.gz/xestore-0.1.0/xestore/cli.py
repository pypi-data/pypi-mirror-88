"""Console script for xestore."""
import sys

import click


@click.command()
def main():
    """Console script for xestore."""
    click.echo("Replace this message by putting your code into "
               "xestore.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
