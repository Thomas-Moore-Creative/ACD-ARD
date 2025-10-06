"""Core utilities for ACD-ARD package."""

from pathlib import Path
from typing import Any, Dict, Optional, cast

import yaml


def load_config(config_name: str, config_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Load a YAML configuration file.

    Args:
        config_name: Name of the config file (without .yml extension)
        config_dir: Directory containing config files. Defaults to config/ in package root.

    Returns:
        Dictionary containing configuration data
    """
    if config_dir is None:
        # Default to config directory relative to package
        config_dir = Path(__file__).parent.parent.parent / "config"

    config_path = config_dir / f"{config_name}.yml"

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r") as f:
        data = yaml.safe_load(f)

    # yaml.safe_load returns Any; ensure a dict for typing correctness
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise TypeError(f"Configuration file is not a mapping: {config_path}")

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
