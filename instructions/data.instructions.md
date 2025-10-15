Zarr / Dataset conventions

## Zarr collections
  - Always use consolidated metadata where possible (consolidated=True) so tools can open the collection efficiently.

- Required dataset attributes
  - `source` : canonical source identifier (e.g., `ACCESS-ESM1-5`)
  - `intake_esm_dataset_key` : intake key used to produce the dataset

- Chunking guidance
  - End goal is usually chunks that include all-time & all-members (if data has ensembles )
  - Steps to get there start with a "base" zarr collection created from the NetCDF archive that writes efficently given both native NetCDF chunking and the time structure of the individual NetCDF files
  - Avoid extremely small chunk sizes that produce millions of tiny files.
  - chunking settings will end up in a config based on experience with the prototype notebooks

- Rechunking and consolidation
  - Begin workflow attempts using the basic .chunk commands
  - If these fail in prototype testing use the `rechunker` library for large-scale rechunking operations; plan an intermediate layout to minimize temporary storage.
  - Consolidate metadata after a write or after re-chunking to ensure efficient open operations.

- Naming rules
  - Be consistent: prefer lowercase, hyphens or underscores for separators, and include version/date only when necessary.
  - Record provenance (who/when/command) in a `README` or `provenance.yml` alongside collections when operations are destructive or long-running.

- Data Safety
  - To address risks of destructive operations on data we will
    - only ever read from the NetCDF archives
    - build zarr collections incrementally at the cost of increased scratch storage space
    