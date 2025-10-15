Zarr / Dataset conventions

## Zarr collections
  - Always use consolidated metadata where possible (consolidated=True) so tools can open the collection efficiently.
  - Layout conventions: prefer a clear hierarchy, e.g.: `<root>/<experiment>/<variable>/<member>.zarr` or `<root>/<variable>.zarr` depending on project needs.

- Required dataset attributes
  - `source` : canonical source identifier (e.g., `ACCESS-ESM1-5`)
  - `intake_esm_dataset_key` : intake key used to produce the dataset
  - `member` : ensemble member id (e.g. `r1i1p1f1`)

- Chunking guidance
  - Time chunking: prefer 1-year or seasonal sized time chunks for monthly data (e.g., 12 months) to balance IO.
  - Spatial chunking: choose blocks that map to natural grid blocks (e.g., 256x256 or similar depending on resolution).
  - Avoid extremely small chunk sizes that produce millions of tiny files.

- Rechunking and consolidation
  - Use the `rechunker` library for large-scale rechunking operations; plan an intermediate layout to minimize temporary storage.
  - Consolidate metadata after a write or after re-chunking to ensure efficient open operations.

- Known sizes and safety
  - Before destructive operations (rebuild/rechunk), generate a `known_sizes.csv` listing each collection and its size. Use this to detect partial writes.
  - Verify the number of keys and the presence of expected attributes before replacing collections.

- Naming rules
  - Be consistent: prefer lowercase, hyphens or underscores for separators, and include version/date only when necessary.
  - Record provenance (who/when/command) in a `README` or `provenance.yml` alongside collections when operations are destructive or long-running.

- Small checklist for ingestion
  - run `intake-esm` catalog search with filters documented
  - create a small sample open to validate dims and coords
  - run chunk / compression checks on sample
  - record output paths and sizes in `known_sizes`