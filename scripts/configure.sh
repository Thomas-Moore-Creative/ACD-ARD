#!/bin/bash
# Configure ACD-ARD environment and paths
# This script sets up the necessary environment variables and validates configuration

set -e

echo "=== ACD-ARD Configuration ==="

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Project root: $PROJECT_ROOT"

# Source configuration if exists
CONFIG_FILE="${PROJECT_ROOT}/config/paths.yml"
if [ -f "$CONFIG_FILE" ]; then
    echo "Configuration file found: $CONFIG_FILE"
else
    echo "Warning: Configuration file not found: $CONFIG_FILE"
fi

# Check for conda environment
if [ -z "$CONDA_DEFAULT_ENV" ]; then
    echo "Warning: No conda environment activated"
    echo "Activate the environment with: conda activate acd_ard"
else
    echo "Active conda environment: $CONDA_DEFAULT_ENV"
fi

# Check if package is installed
if python -c "import acd" 2>/dev/null; then
    echo "ACD package is installed"
    python -c "import acd; print(f'Version: {acd.__version__}')"
else
    echo "Warning: ACD package not installed"
    echo "Install with: pip install -e ."
fi

# Validate configuration files
echo ""
echo "Validating configuration files..."
for config in paths datasets chunks collections parameters; do
    config_file="${PROJECT_ROOT}/config/${config}.yml"
    if [ -f "$config_file" ]; then
        echo "✓ ${config}.yml found"
    else
        echo "✗ ${config}.yml missing"
    fi
done

# Check CLI commands
echo ""
echo "Checking CLI commands..."
for cmd in acd-manifest acd-base acd-rechunk; do
    if command -v "$cmd" &> /dev/null; then
        echo "✓ $cmd available"
    else
        echo "✗ $cmd not found (install package with: pip install -e .)"
    fi
done

echo ""
echo "=== Configuration Complete ==="
