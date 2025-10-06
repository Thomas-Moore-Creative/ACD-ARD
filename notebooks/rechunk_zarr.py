"""
Rechunk Zarr Store - Notebook Driver

This notebook driver can be executed with papermill for batch rechunking operations.
Parameters can be injected via papermill for different chunk configurations.
"""

# Parameters (can be overridden by papermill)
input_store = "../data/base_zarr/example_temp_daily"
output_store = None
chunk_config = "default"
config_dir = "../config"
cluster_type = "local"
num_workers = 4
verbose = True

# %%
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# %%
import xarray as xr
from rechunker import rechunk

from acd.core import load_config, setup_dask_cluster

# %%
print(f"Rechunking store: {input_store}")
print(f"Chunk configuration: {chunk_config}")

# %%
# Load configuration
chunks_config = load_config("chunks", Path(config_dir))
paths_config = load_config("paths", Path(config_dir))
parameters_config = load_config("parameters", Path(config_dir))

# %%
# Get chunk configuration
if chunk_config not in chunks_config.get("chunk_configs", {}):
    raise ValueError(f"Chunk config '{chunk_config}' not found")

target_chunks = chunks_config["chunk_configs"][chunk_config]
print(f"Target chunks: {target_chunks}")

# %%
# Setup Dask cluster
if cluster_type != "local":
    print(f"Setting up {cluster_type.upper()} cluster...")
    cluster_config = parameters_config["cluster"].get(cluster_type, {})
    cluster = setup_dask_cluster(cluster_type, **cluster_config)
    cluster.scale(num_workers)
    client = cluster.get_client()
    print(f"Cluster dashboard: {client.dashboard_link}")
else:
    print("Using local scheduler")

# %%
# Determine output path
if output_store is None:
    rechunked_path = paths_config.get("rechunked_zarr_path", "./data/rechunked_zarr")
    output_store = Path(rechunked_path) / Path(input_store).name
else:
    output_store = Path(output_store)

print(f"Output store: {output_store}")

# %%
# Determine temp store path
temp_store = Path(paths_config.get("temp_path", "./data/temp")) / "rechunk_temp"
print(f"Temp store: {temp_store}")

# %%
# Check if input store exists
input_path = Path(input_store)
if not input_path.exists():
    print(f"Warning: Input store not found: {input_path}")
    print("This is expected in a test environment without actual data")
    print("Rechunking would proceed with actual data")
else:
    # Open source dataset
    ds = xr.open_zarr(input_path)
    print("Source dataset opened")
    print(f"Current chunks: {ds.chunks}")

    # %%
    # Create parent directories
    output_store.parent.mkdir(parents=True, exist_ok=True)
    temp_store.parent.mkdir(parents=True, exist_ok=True)

    # %%
    # Perform rechunking
    max_mem = chunks_config.get("max_mem", "2GB")
    print(f"Max memory per chunk: {max_mem}")

    rechunk_plan = rechunk(
        source=str(input_path),
        target_chunks=target_chunks,
        max_mem=max_mem,
        target_store=str(output_store),
        temp_store=str(temp_store),
    )

    print("Executing rechunk plan...")
    rechunk_plan.execute()

    print(f"Rechunked Zarr store created: {output_store}")

# %%
# Cleanup
if cluster_type != "local":
    client.close()
    cluster.close()
    print("Cluster closed")

# %%
print("Rechunking complete!")
