"""Test configuration for ACD-ARD tests."""

from pathlib import Path

import pytest


@pytest.fixture
def config_dir():
    """Return path to test config directory."""
    return Path(__file__).parent.parent / "config"


@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory for test data."""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return data_dir
