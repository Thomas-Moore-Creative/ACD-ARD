"""Tests for CLI commands."""

from click.testing import CliRunner

from acd_ard.cli import acd_ard  # the group: `acd-ard`


def test_group_help():
    r = CliRunner().invoke(acd_ard, ["--help"])
    assert r.exit_code == 0
    assert "manifest" in r.stdout and "base" in r.stdout and "rechunk" in r.stdout


def test_manifest_help():
    r = CliRunner().invoke(acd_ard, ["manifest", "--help"])
    assert r.exit_code == 0
    assert "--collection" in r.stdout or "-c" in r.stdout


def test_base_help():
    r = CliRunner().invoke(acd_ard, ["base", "--help"])
    assert r.exit_code == 0
    assert "--collection" in r.stdout and "--variable" in r.stdout and "--use-manifest" in r.stdout


def test_rechunk_help():
    r = CliRunner().invoke(acd_ard, ["rechunk", "--help"])
    assert r.exit_code == 0
    assert "--collection" in r.stdout and "--variable" in r.stdout and "--max-mem" in r.stdout


def test_version_option():
    r = CliRunner().invoke(acd_ard, ["--version"])
    # exit code 0 and program name present
    assert r.exit_code == 0
    assert "acd-ard" in r.stdout or "0.0.0" in r.stdout
