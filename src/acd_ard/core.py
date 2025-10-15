"""Core utilities for ACD-ARD package."""

from pathlib import Path
from typing import Any, Dict, Optional, cast

import yaml


def load_config(config_name: str, config_dir: Optional[Path] = None) -> Dict[str, Any]:
    if config_dir is None:
        config_dir = Path(__file__).parent.parent.parent / "config"
    cfg_path = config_dir / f"{config_name}.yml"
    if not cfg_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {cfg_path}")
    data = yaml.safe_load(open(cfg_path))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise TypeError(f"Configuration file is not a mapping: {cfg_path}")
    return cast(Dict[str, Any], data)


def setup_dask_cluster(cluster_type: str = "pbs", **kwargs: Any) -> Any:
    """Setup a Dask cluster for HPC systems.

    Args:
        cluster_type: Type of cluster ('pbs' or 'slurm')
        **kwargs: Additional arguments for cluster configuration

    Returns:
        Dask cluster object
    """
    from dask_jobqueue import PBSCluster, SLURMCluster

    if cluster_type.lower() == "pbs":
        return PBSCluster(**kwargs)
    if cluster_type.lower() == "slurm":
        return SLURMCluster(**kwargs)
    raise ValueError(f"Unsupported cluster type: {cluster_type}")


def start_cluster_from_config(
    profile: str = "default",
    local: bool = False,
    config_dir: Optional[Path] = None,
    **overrides: Any,
) -> Any:
    """Convenience helper to start a Dask cluster from repo config.

    Returns a tuple (client, cluster). When ``local=True`` this starts a
    ``dask.distributed.LocalCluster`` for development and testing.

    Args:
        profile: named cluster profile (currently unused; placeholder for future)
        local: whether to start a LocalCluster instead of a scheduler-backed cluster
        config_dir: optional Path to config directory (passed to ``load_config``)
        **overrides: keyword args passed to the cluster constructor

    Returns:
        (client, cluster) where client is a ``distributed.Client`` and cluster is the
        underlying cluster object (LocalCluster or a jobqueue cluster).
    """
    # import locally to avoid heavy imports at module import time
    if local:
        from dask.distributed import Client, LocalCluster

        cluster = LocalCluster(**overrides)
        client = Client(cluster)
        return client, cluster

    # load cluster parameters from repo config and merge with overrides
    params = load_config("parameters", config_dir)
    cluster_cfg = params.get("cluster", {}) if isinstance(params, dict) else {}
    # determine cluster type: prefer explicit override, then config default
    cluster_type = overrides.pop("cluster_type", None) or cluster_cfg.get("default_type", "pbs")

    # collect profile settings if present
    profile_cfg = cluster_cfg.get(cluster_type, {}) if isinstance(cluster_cfg, dict) else {}
    # merge profile cfg with overrides (overrides win)
    merged = {**profile_cfg, **overrides}

    # create cluster via existing helper
    cluster = setup_dask_cluster(cluster_type=cluster_type, **merged)

    # connect client
    from dask.distributed import Client

    client = Client(cluster)
    return client, cluster
