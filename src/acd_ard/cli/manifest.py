"""acd-manifest - Generate manifest files for NetCDF collections.

This CLI tool scans NetCDF collections and generates manifest files
for processing.
"""

import sys
from pathlib import Path

import click

from acd.cli import common_options
from acd.core import load_config


@click.command()
@click.option("--collection", required=True, help="Name of the collection to process")
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default="manifest.txt",
    help="Output manifest file path",
)
@common_options
def main(collection, output, config_dir, verbose):
    """Generate manifest files for NetCDF collections.

    Scans the specified collection and creates a manifest file listing
    all NetCDF files to be processed.
    """
    try:
        # Load configuration
        collections_config = load_config("collections", config_dir)
        paths_config = load_config("paths", config_dir)

        if verbose:
            click.echo(f"Processing collection: {collection}")
            click.echo(f"Config directory: {config_dir}")

        # Check if collection exists in config
        if collection not in collections_config.get("collections", {}):
            click.echo(f"Error: Collection '{collection}' not found in configuration", err=True)
            sys.exit(1)

        collection_info = collections_config["collections"][collection]

        # Get input path
        input_path = Path(collection_info.get("input_path", ""))
        if not input_path.is_absolute():
            base_path = paths_config.get("base_path", ".")
            input_path = Path(base_path) / input_path

        if verbose:
            click.echo(f"Scanning directory: {input_path}")

        # Generate manifest
        manifest_lines = []
        if input_path.exists():
            nc_files = sorted(input_path.rglob("*.nc"))
            manifest_lines = [str(f) for f in nc_files]

        # Write manifest
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            f.write("\n".join(manifest_lines))

        click.echo(f"Manifest written to: {output_path}")
        click.echo(f"Total files: {len(manifest_lines)}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        if verbose:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
