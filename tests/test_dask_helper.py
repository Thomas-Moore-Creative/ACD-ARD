"""Lightweight tests for dask helpers.

These tests start a minimal LocalCluster to validate the helper function.
They are deliberately small and use 1 worker to be CI-friendly.
"""

from acd_ard.core import start_cluster_from_config


def test_start_threaded_client():
    """Start a lightweight threaded client (no worker processes) to keep the test fast."""
    # Request a client with processes=False (threaded) via overrides
    client, cluster = start_cluster_from_config(
        local=True, n_workers=1, threads_per_worker=1, processes=False
    )
    try:
        fut = client.submit(lambda: 1 + 2)
        assert fut.result(timeout=5) == 3
    finally:
        client.close()
        # LocalCluster may not expose close on some configs; guard it
        try:
            cluster.close()
        except Exception:
            pass
