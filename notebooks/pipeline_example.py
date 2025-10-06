"""
Pipeline Example - Complete Workflow

This notebook demonstrates the complete ACD-ARD pipeline:
1. Generate manifest
2. Convert to base Zarr
3. Rechunk for optimal access
"""

# Parameters
collection_name = "nci_temperature"
dataset_name = "example_temp_daily"
chunk_config = "default"
config_dir = "../config"

# %%
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# %%
from acd.core import load_config

# %%
print("=== ACD-ARD Pipeline Example ===")
print(f"Collection: {collection_name}")
print(f"Dataset: {dataset_name}")
print(f"Chunk config: {chunk_config}")

# %%
# Load all configurations
config_path = Path(config_dir)

collections_config = load_config('collections', config_path)
datasets_config = load_config('datasets', config_path)
chunks_config = load_config('chunks', config_path)
paths_config = load_config('paths', config_path)
parameters_config = load_config('parameters', config_path)

print("\nConfigurations loaded successfully")

# %%
# Display collection info
if collection_name in collections_config.get('collections', {}):
    collection_info = collections_config['collections'][collection_name]
    print(f"\nCollection: {collection_info.get('description', 'N/A')}")
    print(f"Datasets in collection: {collection_info.get('datasets', [])}")
else:
    print(f"\nWarning: Collection '{collection_name}' not found")

# %%
# Display dataset info
if dataset_name in datasets_config.get('datasets', {}):
    dataset_info = datasets_config['datasets'][dataset_name]
    print(f"\nDataset: {dataset_info.get('description', 'N/A')}")
    print(f"Variables: {dataset_info.get('variables', [])}")
    print(f"Time range: {dataset_info.get('time_range', {})}")
else:
    print(f"\nWarning: Dataset '{dataset_name}' not found")

# %%
# Display chunk configuration
if chunk_config in chunks_config.get('chunk_configs', {}):
    chunk_info = chunks_config['chunk_configs'][chunk_config]
    print(f"\nChunk configuration '{chunk_config}':")
    for dim, size in chunk_info.items():
        print(f"  {dim}: {size}")
else:
    print(f"\nWarning: Chunk config '{chunk_config}' not found")

# %%
# Display processing parameters
print("\nProcessing parameters:")
print(f"Cluster type: {parameters_config.get('cluster', {}).get('default_type', 'N/A')}")
print(f"Max workers: {parameters_config.get('parallel', {}).get('max_workers', 'N/A')}")
print(f"Zarr compressor: {parameters_config.get('zarr_encoding', {}).get('compressor', {}).get('cname', 'N/A')}")

# %%
print("\n=== Pipeline Configuration Complete ===")
print("\nNext steps:")
print("1. Run: acd-manifest --collection", collection_name)
print("2. Run: acd-base --dataset", dataset_name)
print("3. Run: acd-rechunk --input <base_zarr> --chunks-config", chunk_config)
print("\nOr use: scripts/run_pipeline.sh to run all steps")
