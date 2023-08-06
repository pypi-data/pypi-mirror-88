"""
The root of the command hierarchy.
"""
import click


@click.group()
@click.version_option()
def cli() -> None:
    """
    A weather cli.
    """
