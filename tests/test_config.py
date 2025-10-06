"""Tests for configuration files."""

import yaml


def test_paths_config_structure(config_dir):
    """Test paths.yml has required structure."""
    config_path = config_dir / "paths.yml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    required_keys = [
        "base_path",
        "base_zarr_path",
        "rechunked_zarr_path",
        "temp_path",
        "manifest_path",
        "logs_path",
    ]

    for key in required_keys:
        assert key in config, f"Missing key: {key}"


def test_datasets_config_structure(config_dir):
    """Test datasets.yml has required structure."""
    config_path = config_dir / "datasets.yml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    assert "datasets" in config
    assert len(config["datasets"]) > 0

    # Check first dataset has required fields
    first_dataset = list(config["datasets"].values())[0]
    assert "description" in first_dataset
    assert "input_path" in first_dataset


def test_chunks_config_structure(config_dir):
    """Test chunks.yml has required structure."""
    config_path = config_dir / "chunks.yml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    assert "chunk_configs" in config
    assert "default" in config["chunk_configs"]

    # Check default config has dimension specifications
    default_chunks = config["chunk_configs"]["default"]
    assert "time" in default_chunks
    assert "lat" in default_chunks
    assert "lon" in default_chunks


def test_collections_config_structure(config_dir):
    """Test collections.yml has required structure."""
    config_path = config_dir / "collections.yml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    assert "collections" in config
    assert len(config["collections"]) > 0


def test_parameters_config_structure(config_dir):
    """Test parameters.yml has required structure."""
    config_path = config_dir / "parameters.yml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    required_sections = ["cluster", "zarr_encoding", "rechunking", "parallel"]

    for section in required_sections:
        assert section in config, f"Missing section: {section}"
