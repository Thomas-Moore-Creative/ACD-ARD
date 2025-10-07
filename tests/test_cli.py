"""Tests for CLI commands."""

from click.testing import CliRunner

from acd_ard.cli.base import main as base_main
from acd_ard.cli.manifest import main as manifest_main
from acd_ard.cli.rechunk import main as rechunk_main


def test_manifest_cli_help():
    """Test manifest CLI help output."""
    runner = CliRunner()
    result = runner.invoke(manifest_main, ["--help"])
    assert result.exit_code == 0
    assert "Generate manifest files" in result.output


def test_base_cli_help():
    """Test base CLI help output."""
    runner = CliRunner()
    result = runner.invoke(base_main, ["--help"])
    assert result.exit_code == 0
    assert "Convert NetCDF archives" in result.output


def test_rechunk_cli_help():
    """Test rechunk CLI help output."""
    runner = CliRunner()
    result = runner.invoke(rechunk_main, ["--help"])
    assert result.exit_code == 0
    assert "Rechunk Zarr stores" in result.output


def test_manifest_missing_collection(config_dir):
    """Test manifest CLI with missing collection."""
    runner = CliRunner()
    result = runner.invoke(
        manifest_main, ["--collection", "nonexistent", "--config-dir", str(config_dir)]
    )
    assert result.exit_code != 0


def test_base_missing_dataset(config_dir):
    """Test base CLI with missing dataset."""
    runner = CliRunner()
    result = runner.invoke(base_main, ["--dataset", "nonexistent", "--config-dir", str(config_dir)])
    assert result.exit_code != 0
