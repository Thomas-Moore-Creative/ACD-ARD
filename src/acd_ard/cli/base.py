"""acd-base - Convert NetCDF archives to base Zarr format.

This CLI tool converts NetCDF collections to base Zarr format using Dask
for distributed processing on HPC systems.
"""

import sys
from pathlib import Path

import click
import xarray as xr

from acd.cli import common_options
from acd.core import load_config, setup_dask_cluster


@click.command()
@click.option("--dataset", required=True, help="Name of the dataset to process")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output Zarr store path")
@click.option(
    "--cluster-type",
    type=click.Choice(["pbs", "slurm", "local"]),
    default="local",
    help="Dask cluster type",
)
@click.option("--workers", type=int, default=4, help="Number of workers")
@common_options
def main(dataset, output, cluster_type, workers, config_dir, verbose):
    """Convert NetCDF archives to base Zarr format.

    Reads NetCDF files and converts them to Zarr format using Dask
    for parallel processing on HPC systems.
    """
    try:
        # Load configuration
        datasets_config = load_config("datasets", config_dir)
        paths_config = load_config("paths", config_dir)

        if verbose:
            click.echo(f"Processing dataset: {dataset}")
            click.echo(f"Cluster type: {cluster_type}")

        # Check if dataset exists in config
        if dataset not in datasets_config.get("datasets", {}):
            click.echo(f"Error: Dataset '{dataset}' not found in configuration", err=True)
            sys.exit(1)

        dataset_info = datasets_config["datasets"][dataset]

        # Determine output path
        if output is None:
            base_output = paths_config.get("base_zarr_path", "./data/base_zarr")
            output = Path(base_output) / dataset
        else:
            output = Path(output)

        if verbose:
            click.echo(f"Output path: {output}")

        # Setup Dask cluster if not local
        if cluster_type != "local":
            if verbose:
                click.echo(f"Setting up {cluster_type.upper()} cluster...")
            cluster = setup_dask_cluster(cluster_type, cores=1, memory="4GB")
            cluster.scale(workers)
            client = cluster.get_client()
            if verbose:
                click.echo(f"Cluster dashboard: {client.dashboard_link}")

        # Get input files
        input_path = dataset_info.get("input_path", "")
        input_files = dataset_info.get("files", [])

        if isinstance(input_files, str):
            input_files = [input_files]

        if verbose:
            click.echo(f"Input files: {len(input_files) if input_files else 'pattern-based'}")

        # Open dataset
        if input_files:
            ds = xr.open_mfdataset(input_files, combine="by_coords", parallel=True)
        else:
            ds = xr.open_mfdataset(f"{input_path}/*.nc", combine="by_coords", parallel=True)

        if verbose:
            click.echo(f"Dataset shape: {ds.dims}")

        # Write to Zarr
        output.parent.mkdir(parents=True, exist_ok=True)
        ds.to_zarr(output, mode="w", consolidated=True)

        click.echo(f"Base Zarr store created: {output}")

        if cluster_type != "local":
            client.close()
            cluster.close()

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        if verbose:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
