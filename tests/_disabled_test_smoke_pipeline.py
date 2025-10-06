from pathlib import Path
from subprocess import check_call

import numpy as np
import xarray as xr
import yaml

# ensure package is imported for coverage, regardless of folder name
try:
    import acd  # noqa: F401
except ImportError:
    import acd_ard as acd  # noqa: F401


def test_smoke(tmp_path):
    # ----- 1) tiny inputs -----
    inputs = tmp_path / "inputs"
    (inputs / "tas").mkdir(parents=True, exist_ok=True)
    (inputs / "pr").mkdir(parents=True, exist_ok=True)

    time = np.arange("2000-01", "2000-04", dtype="datetime64[M]")  # 3 months
    lat = np.linspace(-45, -44, 2)
    lon = np.linspace(150, 152, 3)

    def write(var: str) -> None:
        ds = xr.Dataset(
            {var: (("time", "lat", "lon"), np.random.rand(time.size, lat.size, lon.size))},
            coords={"time": time, "lat": lat, "lon": lon},
        )
        ds.to_netcdf(inputs / var / f"{var}.nc")

    for v in ("tas", "pr"):
        write(v)

    # ----- 2) localise config to tmp dirs -----
    proj = tmp_path / "proj"
    scratch = tmp_path / "scratch"
    paths = {
        "project_root": str(proj),
        "scratch_root": str(scratch),
        "manifests": f"{proj}/manifests",
        "logs": f"{proj}/logs",
        "notebooks": f"{proj}/notebooks",
        "zarr_base": f"{scratch}/zarr/base",
        "zarr_custom": f"{scratch}/zarr/custom",
        "rechunk_tmp": f"{scratch}/tmp_rechunk",
        "dask_spill": f"{scratch}/dask/worker-spill",
    }
    Path("config/paths.yml").write_text(yaml.safe_dump(paths, sort_keys=False))

    datasets = {"roots": {"SYNTH": str(inputs)}, "engine": {"SYNTH": "h5netcdf"}}
    Path("config/datasets.yml").write_text(yaml.safe_dump(datasets, sort_keys=False))

    collections = {
        "collections": {
            "synthetic": {
                "dataset": "SYNTH",
                "variables": ["tas", "pr"],
                "pattern": "{variable}/*.nc",
            }
        }
    }
    Path("config/collections.yml").write_text(yaml.safe_dump(collections, sort_keys=False))

    # ----- 3) run the pipeline -----
    check_call(["acd-manifest", "--collection", "synthetic"])
    check_call(["acd-base", "--collection", "synthetic", "--variable", "tas"])
    check_call(
        [
            "acd-rechunk",
            "--collection",
            "synthetic",
            "--variable",
            "tas",
            "--max-mem",
            "512MB",
        ]
    )

    # ----- 4) validate outputs -----
    z = scratch / "zarr" / "custom" / "synthetic" / "tas.zarr"
    assert (z / ".zmetadata").exists()
    ds = xr.open_zarr(z, consolidated=True)
    assert ds.tas.shape == (3, 2, 3)
    _ = float(ds.tas.mean().compute())  # tiny compute to prove stack works
