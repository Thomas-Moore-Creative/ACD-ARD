import sys

import click


@click.command(
    help="acd-ard: write base Zarr for a variable in a collection.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.option("--collection", "-c", required=True, metavar="NAME", help="Collection name")
@click.option("--variable", "-v", required=True, metavar="VAR", help="Variable name")
@click.option("--use-manifest", is_flag=True, help="Use pre-built parquet manifest")
def base(collection: str, variable: str, use_manifest: bool) -> None:
    click.echo(
        f"OK: would write base Zarr for {collection}:{variable} (use_manifest={use_manifest})"
    )
    sys.exit(0)
