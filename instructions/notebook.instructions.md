# Notebook & papermill guidance

- Use notebooks for exploration; convert reproducible workflows into scripts for production.
- For parameterised runs use `papermill` and record parameters and outputs as artifacts.
- Strip large outputs before committing; keep notebooks small and focused.
- Use an environment that matches project dependencies; record kernel info in notebook metadata.
- Prefer `nbformat` checks in CI if notebooks are committed.