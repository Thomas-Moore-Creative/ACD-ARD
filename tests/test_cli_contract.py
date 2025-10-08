import subprocess

def _out(cmd):  # helper
    return subprocess.run(cmd + ["--help"], capture_output=True, text=True, check=True).stdout

def test_group_help_branding_and_subcommands():
    txt = _out(["acd-ard"])
    assert "ACD-ARD" in txt  # brand visible
    assert "manifest" in txt and "base" in txt and "rechunk" in txt

def test_manifest_flags_present():
    txt = _out(["acd-ard", "manifest"])
    assert "--collection" in txt or "-c" in txt

def test_base_flags_present():
    txt = _out(["acd-ard", "base"])
    assert "--collection" in txt and "--variable" in txt and "--use-manifest" in txt

def test_rechunk_flags_present():
    txt = _out(["acd-ard", "rechunk"])
    assert "--collection" in txt and "--variable" in txt and "--max-mem" in txt
