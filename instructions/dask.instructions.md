Dask configuration and run patterns

Local development

- Use `dask.distributed.LocalCluster` for testing and small jobs.
- Configure `n_workers`, `threads_per_worker`, and memory per worker to match local machine.

HPC / jobqueue

- Use `dask-jobqueue` (PBS, SLURM, etc.) when running on a cluster; keep resource profiles in a config file.
- Request sufficient walltime and memory; oversubscribe CPU only when IO-bound.

Chunking and task graph planning

- Rechunk only when necessary; plan intermediate chunk sizes.
- Use `dask.array`/`xarray` diagnostics to inspect task graph and estimate intermediate storage requirements.

Monitoring and logging

- Enable the dashboard for long-running jobs; capture worker logs to central location.
- Set `distributed.comm.timeouts` and retry settings for flaky clusters.

Best practices

- Avoid creating extremely large numbers of small tasks; increase chunk size to amortize task overhead.
- Move heavy IO tasks onto fewer workers with larger memory to reduce shuffling.
- Use data locality where possible (run compute near data).

Reproducibility

- Pin dask and distributed versions for experiments; record the environment in job logs.
- Use dask config files for cluster profiles in repo under `config/`.