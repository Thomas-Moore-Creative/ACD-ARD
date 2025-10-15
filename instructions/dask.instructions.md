Dask configuration and run patterns

Local development

- Use `dask.distributed.LocalCluster` for testing and small jobs.
- Configure `n_workers`, `threads_per_worker`, and memory per worker to match local machine.

HPC

- HPC will be ARE-based jupyter notebook prototypes that will be made operational and CLI-ready using papermill
- Use `dask.distributed.LocalCluster`
- Configure `n_workers`, `threads_per_worker`, and memory per worker to match local machine.

Chunking

- Rechunking will be a core function of this codebase.
- Settings should be controlled via a config

Best practices

- Avoid creating extremely large numbers of small tasks; increase chunk size to amortize task overhead.
- Move heavy IO tasks onto fewer workers with larger memory to reduce shuffling.
- Use data locality where possible (run compute near data).

Reproducibility

- Pin dask and distributed versions for experiments; record the environment in job logs.
- Use dask config files for cluster profiles in repo under `config/`.

Quick LocalCluster example

```python
# start a minimal local cluster for testing
from acd_ard.core import start_cluster_from_config

client, cluster = start_cluster_from_config(local=True, n_workers=1, threads_per_worker=1)
# run work
fut = client.submit(lambda: 1 + 1)
assert fut.result() == 2
# cleanup
client.close()
cluster.close()
```