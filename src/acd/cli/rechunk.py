"""acd-rechunk - Rechunk Zarr stores with custom chunk sizes.

This CLI tool rechunks existing Zarr stores to optimize for specific
access patterns using the rechunker library.
"""

import sys
from pathlib import Path

import click
import xarray as xr
from rechunker import rechunk

from acd.cli import common_options
from acd.core import load_config, setup_dask_cluster


@click.command()
@click.option(
    "--input",
    "-i",
    "input_store",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Input Zarr store path",
)
@click.option(
    "--output", "-o", type=click.Path(path_type=Path), help="Output rechunked Zarr store path"
)
@click.option("--chunks-config", default="default", help="Chunk configuration name from chunks.yml")
@click.option(
    "--cluster-type",
    type=click.Choice(["pbs", "slurm", "local"]),
    default="local",
    help="Dask cluster type",
)
@click.option("--workers", type=int, default=4, help="Number of workers")
@click.option(
    "--temp-store", type=click.Path(path_type=Path), help="Temporary store path for rechunking"
)
@common_options
def main(
    input_store, output, chunks_config, cluster_type, workers, temp_store, config_dir, verbose
):
    """Rechunk Zarr stores with custom chunk sizes.

    Reads an existing Zarr store and rechunks it according to the specified
    chunk configuration for optimized access patterns.
    """
    try:
        # Load configuration
        chunks_cfg = load_config("chunks", config_dir)
        paths_config = load_config("paths", config_dir)

        if verbose:
            click.echo(f"Input store: {input_store}")
            click.echo(f"Chunk configuration: {chunks_config}")

        # Get chunk configuration
        if chunks_config not in chunks_cfg.get("chunk_configs", {}):
            click.echo(f"Error: Chunk config '{chunks_config}' not found", err=True)
            sys.exit(1)

        target_chunks = chunks_cfg["chunk_configs"][chunks_config]

        # Determine output path
        if output is None:
            rechunked_path = paths_config.get("rechunked_zarr_path", "./data/rechunked_zarr")
            output = Path(rechunked_path) / input_store.name
        else:
            output = Path(output)

        # Determine temp store path
        if temp_store is None:
            temp_store = Path(paths_config.get("temp_path", "./data/temp")) / "rechunk_temp"
        else:
            temp_store = Path(temp_store)

        if verbose:
            click.echo(f"Output path: {output}")
            click.echo(f"Temp store: {temp_store}")

        # Setup Dask cluster if not local
        if cluster_type != "local":
            if verbose:
                click.echo(f"Setting up {cluster_type.upper()} cluster...")
            cluster = setup_dask_cluster(cluster_type, cores=1, memory="4GB")
            cluster.scale(workers)
            client = cluster.get_client()
            if verbose:
                click.echo(f"Cluster dashboard: {client.dashboard_link}")

        # Open source dataset
        ds = xr.open_zarr(input_store)

        if verbose:
            click.echo(f"Source chunks: {ds.chunks}")
            click.echo(f"Target chunks: {target_chunks}")

        # Create parent directories
        output.parent.mkdir(parents=True, exist_ok=True)
        temp_store.parent.mkdir(parents=True, exist_ok=True)

        # Perform rechunking
        max_mem = chunks_cfg.get("max_mem", "2GB")

        rechunk_plan = rechunk(
            source=input_store,
            target_chunks=target_chunks,
            max_mem=max_mem,
            target_store=str(output),
            temp_store=str(temp_store),
        )

        if verbose:
            click.echo("Executing rechunk plan...")

        rechunk_plan.execute()

        click.echo(f"Rechunked Zarr store created: {output}")

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
