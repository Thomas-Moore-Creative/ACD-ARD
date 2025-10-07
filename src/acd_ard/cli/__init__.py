"""CLI utilities for ACD commands."""

import importlib.metadata as _md
import click
from .manifest import manifest
from .base import base
from .rechunk import rechunk

_VERSION = _md.version("acd_ard")

@click.group(
    help="ACD-ARD: Australian Climate Data — Analysis-Ready Data tools.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.version_option(version=_VERSION, prog_name="acd-ard")
def acd_ard() -> None:
    """Top-level command for all ACD-ARD tooling."""
    # no body needed; Click uses this as the entry point

# Subcommands stay short; users invoke via `acd-ard …`
acd_ard.add_command(manifest, name="manifest")
acd_ard.add_command(base, name="base")
acd_ard.add_command(rechunk, name="rechunk")

