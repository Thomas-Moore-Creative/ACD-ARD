#!/bin/bash
# Run the complete ACD-ARD pipeline
# Orchestrates manifest generation, base conversion, and rechunking

set -e

echo "=== ACD-ARD Pipeline Execution ==="

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default parameters (can be overridden by environment variables)
COLLECTION="${COLLECTION:-australian_climate_reanalysis}"
DATASET="${DATASET:-example_temp_daily}"
CHUNK_CONFIG="${CHUNK_CONFIG:-default}"
CLUSTER_TYPE="${CLUSTER_TYPE:-local}"
WORKERS="${WORKERS:-4}"
CONFIG_DIR="${CONFIG_DIR:-${PROJECT_ROOT}/config}"
VERBOSE="${VERBOSE:-}"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --collection)
            COLLECTION="$2"
            shift 2
            ;;
        --dataset)
            DATASET="$2"
            shift 2
            ;;
        --chunk-config)
            CHUNK_CONFIG="$2"
            shift 2
            ;;
        --cluster-type)
            CLUSTER_TYPE="$2"
            shift 2
            ;;
        --workers)
            WORKERS="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="-v"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--collection NAME] [--dataset NAME] [--chunk-config NAME] [--cluster-type TYPE] [--workers N] [-v]"
            exit 1
            ;;
    esac
done

echo "Configuration:"
echo "  Collection: $COLLECTION"
echo "  Dataset: $DATASET"
echo "  Chunk Config: $CHUNK_CONFIG"
echo "  Cluster Type: $CLUSTER_TYPE"
echo "  Workers: $WORKERS"
echo ""

# Step 1: Generate manifest
echo "Step 1/3: Generating manifest..."
acd-manifest \
    --collection "$COLLECTION" \
    --config-dir "$CONFIG_DIR" \
    --output "${PROJECT_ROOT}/manifests/${COLLECTION}.txt" \
    $VERBOSE

# Step 2: Convert to base Zarr
echo ""
echo "Step 2/3: Converting to base Zarr..."
acd-base \
    --dataset "$DATASET" \
    --cluster-type "$CLUSTER_TYPE" \
    --workers "$WORKERS" \
    --config-dir "$CONFIG_DIR" \
    $VERBOSE

# Step 3: Rechunk
echo ""
echo "Step 3/3: Rechunking..."

# Get the output path from base conversion (simplified - would need to parse config)
BASE_ZARR_PATH="${PROJECT_ROOT}/data/base_zarr/${DATASET}"

if [ -d "$BASE_ZARR_PATH" ]; then
    acd-rechunk \
        --input "$BASE_ZARR_PATH" \
        --chunks-config "$CHUNK_CONFIG" \
        --cluster-type "$CLUSTER_TYPE" \
        --workers "$WORKERS" \
        --config-dir "$CONFIG_DIR" \
        $VERBOSE
else
    echo "Warning: Base Zarr path not found: $BASE_ZARR_PATH"
    echo "Skipping rechunking step"
fi

echo ""
echo "=== Pipeline Complete ==="
