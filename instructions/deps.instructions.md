# Dependency and packaging rules

## Development environment

- Use `pip install -e '.[dev]'` to install development extras.
- Pin versions for reproducible development; prefer a `requirements-dev.txt` or use `pip-tools`.

## Runtime dependencies

- Keep runtime dependencies minimal; mark optional extras in `pyproject.toml`.


## Packaging

- Use `pyproject.toml` for package metadata and `project.scripts` for CLI entry points.
- Provide tests for any script/console entry point.