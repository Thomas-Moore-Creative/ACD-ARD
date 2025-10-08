"""Tests for core functionality."""

import pytest

from acd_ard.core import load_config, setup_dask_cluster


def test_load_config(config_dir):
    """Test loading configuration files."""
    # Test loading paths config
    paths = load_config("paths", config_dir)
    assert "base_path" in paths
    assert "base_zarr_path" in paths

    # Test loading datasets config
    datasets = load_config("datasets", config_dir)
    assert "datasets" in datasets

    # Test loading chunks config
    chunks = load_config("chunks", config_dir)
    assert "chunk_configs" in chunks
    assert "default" in chunks["chunk_configs"]


def test_load_config_not_found(config_dir):
    """Test loading non-existent config raises error."""
    with pytest.raises(FileNotFoundError):
        load_config("nonexistent", config_dir)


def test_setup_dask_cluster_unsupported():
    """Test setup_dask_cluster with unsupported type raises error."""
    with pytest.raises(ValueError, match="Unsupported cluster type"):
        setup_dask_cluster("unsupported")
