import sys

import click


@click.command(
    help="acd-ard: build parquet manifest(s) of input NetCDF files.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.option("--collection", "-c", metavar="NAME", help="Collection name (default: all)")
def manifest(collection: str | None) -> None:
    targets = [collection] if collection else ["<ALL>"]
    click.echo("OK: would build manifests for: " + ", ".join(targets))
    sys.exit(0)
