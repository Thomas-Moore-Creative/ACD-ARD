"""CLI utilities for ACD commands."""

import click
from importlib.metadata import PackageNotFoundError, version

from .manifest import manifest
from .base import base
from .rechunk import rechunk

def _get_version() -> str:
    # Try the distribution names first (hyphen is the canonical project name)
    for dist in ("acd-ard", "acd_ard"):
        try:
            return version(dist)
        except PackageNotFoundError:
            pass
    # Fallback to module attr if defined, else a dev marker
    try:
        from .. import __version__
        return __version__
    except Exception:
        return "0.0.0+local"

@click.group(
    help="ACD-ARD: Australian Climate Data — Analysis-Ready Data tools.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.version_option(version=_get_version(), prog_name="acd-ard")
def acd_ard() -> None:
    """ACD-ARD command group (top-level CLI group)."""
    pass
# Subcommands stay short; users invoke via `acd-ard …`
acd_ard.add_command(manifest, name="manifest")
acd_ard.add_command(base, name="base")
acd_ard.add_command(rechunk, name="rechunk")

