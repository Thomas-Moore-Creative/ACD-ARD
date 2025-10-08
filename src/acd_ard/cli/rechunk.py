import sys
import click

@click.command(
    help="acd-ard: rechunk a base Zarr into a custom-chunked Zarr.",
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.option("--collection", "-c", required=True, metavar="NAME", help="Collection name")
@click.option("--variable", "-v", required=True, metavar="VAR", help="Variable name")
@click.option("--max-mem", default="8GB", show_default=True, help="Per-worker memory budget")
def rechunk(collection: str, variable: str, max_mem: str) -> None:
    click.echo(f"OK: would rechunk {collection}:{variable} with max_mem={max_mem}")
    sys.exit(0)
