# ACD-ARD

Analysis-ready data workflows (ARD) for Australian Climate Data - primarily large NetCDF collections at NCI.

This package provides tools for converting NetCDF climate archives to Zarr format using Dask for distributed processing on HPC systems (PBS/Slurm).

## Features

- **NetCDF to Zarr Conversion**: Convert large NetCDF collections to base Zarr format
- **Custom Rechunking**: Optimize Zarr stores with custom chunk sizes for specific access patterns
- **HPC Integration**: Support for PBS and Slurm job schedulers via dask-jobqueue
- **Manifest Generation**: Scan and catalog NetCDF collections
- **Papermill Integration**: Execute notebooks programmatically for batch processing
- **Configuration-driven**: YAML-based configuration for datasets, chunks, and processing parameters

## Installation

### Using conda (recommended)

```bash
# Create environment from file
conda env create -f envs/acd_ard.yml
conda activate acd_ard

# Install package in development mode
pip install -e .
```

### Using pip

```bash
pip install -e .
```

## Quick Start

### 1. Configure paths

Edit `config/paths.yml` to set up your data directories:

```yaml
base_path: /scratch/data
input_base_path: /g/data/climate/netcdf
base_zarr_path: /scratch/data/zarr/base
rechunked_zarr_path: /scratch/data/zarr/rechunked
```

### 2. Initialize directory layout

```bash
./scripts/init_layout.sh
```

### 3. Run the pipeline

```bash
# Run complete pipeline with defaults
./scripts/run_pipeline.sh

# Or run with custom parameters
./scripts/run_pipeline.sh \
  --collection nci_temperature \
  --dataset example_temp_daily \
  --chunk-config spatial \
  --cluster-type pbs \
  --workers 10
```

## CLI Commands

### acd-manifest

Generate manifest files for NetCDF collections:

```bash
acd-manifest --collection nci_temperature --output manifests/temp.txt
```

### acd-base

Convert NetCDF archives to base Zarr format:

```bash
acd-base --dataset example_temp_daily --cluster-type pbs --workers 8
```

### acd-rechunk

Rechunk Zarr stores with custom chunk sizes:

```bash
acd-rechunk \
  --input data/base_zarr/example_temp_daily \
  --chunks-config timeseries \
  --cluster-type pbs
```

## Configuration

### Datasets (`config/datasets.yml`)

Define datasets to process:

```yaml
datasets:
  example_temp_daily:
    description: "Example daily temperature dataset"
    input_path: /g/data/climate/netcdf/temp/daily
    variables: [temp, temp_min, temp_max]
```

### Chunks (`config/chunks.yml`)

Define chunk configurations for different use cases:

```yaml
chunk_configs:
  timeseries:  # Optimized for temporal analysis
    time: 3650
    lat: 50
    lon: 50
  spatial:     # Optimized for spatial analysis
    time: 30
    lat: 500
    lon: 500
```

### Collections (`config/collections.yml`)

Group related datasets:

```yaml
collections:
  nci_temperature:
    description: "NCI temperature datasets collection"
    datasets: [example_temp_daily]
    input_path: /g/data/climate/netcdf/temp
```

### Parameters (`config/parameters.yml`)

Configure processing parameters:

```yaml
cluster:
  default_type: pbs
  pbs:
    queue: normal
    project: w40
    walltime: "02:00:00"
    cores: 4
    memory: "16GB"
```

## Notebooks

The `notebooks/` directory contains Python notebook drivers that can be executed with papermill:

- `convert_to_base_zarr.py`: Convert NetCDF to base Zarr
- `rechunk_zarr.py`: Rechunk Zarr stores
- `pipeline_example.py`: Complete pipeline example

Execute with papermill:

```bash
papermill notebooks/convert_to_base_zarr.py output.ipynb \
  -p dataset_name example_temp_daily \
  -p cluster_type pbs
```

## Development

### Running tests

```bash
pytest tests/ -v
```

### Linting

```bash
ruff check src/ tests/
```

## Project Structure

```
ACD-ARD/
├── src/acd/           # Main package
│   ├── cli/           # CLI commands
│   ├── core.py        # Core utilities
│   └── __init__.py
├── config/            # Configuration files
│   ├── paths.yml
│   ├── datasets.yml
│   ├── chunks.yml
│   ├── collections.yml
│   └── parameters.yml
├── scripts/           # Shell scripts
│   ├── configure.sh
│   ├── init_layout.sh
│   └── run_pipeline.sh
├── notebooks/         # Notebook drivers
├── tests/             # Tests
├── envs/              # Conda environment
└── pyproject.toml     # Package configuration
```

## License

MIT License - see LICENSE file for details.
