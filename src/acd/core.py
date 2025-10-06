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
