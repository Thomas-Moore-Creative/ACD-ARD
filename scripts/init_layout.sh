#!/bin/bash
# Initialize directory layout for ACD-ARD pipeline
# Creates necessary directories for data processing

set -e

echo "=== Initializing ACD-ARD Directory Layout ==="

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Load paths from configuration
# Default paths (can be overridden)
BASE_PATH="${BASE_PATH:-/scratch/data}"
INPUT_BASE="${INPUT_BASE:-/g/data/climate/netcdf}"
BASE_ZARR="${BASE_ZARR:-${BASE_PATH}/zarr/base}"
RECHUNKED_ZARR="${RECHUNKED_ZARR:-${BASE_PATH}/zarr/rechunked}"
TEMP_PATH="${TEMP_PATH:-${BASE_PATH}/temp}"
MANIFEST_PATH="${MANIFEST_PATH:-${BASE_PATH}/manifests}"
LOGS_PATH="${LOGS_PATH:-${BASE_PATH}/logs}"

echo "Creating directories..."

# Create output directories
mkdir -p "$BASE_ZARR"
echo "✓ Created: $BASE_ZARR"

mkdir -p "$RECHUNKED_ZARR"
echo "✓ Created: $RECHUNKED_ZARR"

mkdir -p "$TEMP_PATH"
echo "✓ Created: $TEMP_PATH"

mkdir -p "$MANIFEST_PATH"
echo "✓ Created: $MANIFEST_PATH"

mkdir -p "$LOGS_PATH"
echo "✓ Created: $LOGS_PATH"

# Set permissions (adjust as needed for your HPC environment)
chmod -R 755 "$BASE_PATH" 2>/dev/null || echo "Note: Could not set permissions (may need root)"

echo ""
echo "=== Directory Layout Complete ==="
echo "Base path: $BASE_PATH"
echo "Base Zarr: $BASE_ZARR"
echo "Rechunked Zarr: $RECHUNKED_ZARR"
echo "Temp: $TEMP_PATH"
echo "Manifests: $MANIFEST_PATH"
echo "Logs: $LOGS_PATH"
