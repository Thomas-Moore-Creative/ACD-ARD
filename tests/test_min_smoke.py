from pathlib import Path

# ensure your package is imported
import acd_ard as pkg  # noqa: F401

def test_minimal_zarr_roundtrip(tmp_path: Path):
    # No CLIs, no configs — just verify xarray↔zarr stack works
    import numpy as np
    import xarray as xr

    time = np.arange("2000-01", "2000-03", dtype="datetime64[M]")
    lat = np.linspace(-45, -44, 2)
    lon = np.linspace(150, 151, 2)

    ds = xr.Dataset(
        {"tas": (("time", "lat", "lon"), np.random.rand(time.size, lat.size, lon.size))},
        coords={"time": time, "lat": lat, "lon": lon},
    )

    store = tmp_path / "tas.zarr"
    ds.to_zarr(store, mode="w", consolidated=True)
    ds2 = xr.open_zarr(store, consolidated=True)

    assert ds2.tas.shape == (2, 2, 2)
    assert float(ds2.tas.mean().compute()) >= 0.0
