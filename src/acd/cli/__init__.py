"""CLI utilities for ACD commands."""

from pathlib import Path

import click


def common_options(func):
    """Common CLI options decorator."""
    func = click.option(
        '--config-dir',
        type=click.Path(exists=True, file_okay=False, path_type=Path),
        default='config',
        help='Directory containing configuration files'
    )(func)
    func = click.option(
        '--verbose', '-v',
        is_flag=True,
        help='Enable verbose output'
    )(func)
    return func
