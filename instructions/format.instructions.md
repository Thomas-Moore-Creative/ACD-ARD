# Formatting & linting

## Formatting

- Use `black` for deterministic formatting: `black .` (CI uses `black --check`).

## Linting

- Use `ruff` for linting and many auto-fixes: `ruff check --fix .`.
- Keep `pyproject.toml` configuration for ruff rules and ignored codes.

## Type checking

- Optionally run `mypy` if the project uses typing.

## Recommended local workflow

- `ruff check --fix .`
- `black .`
- `ruff check .` to confirm no remaining issues

## Pre-commit (disabled)

- currently NOT enabled
- quick commands to enable pre-commit in the future:

    Add .pre-commit-config.yaml (ruff + black).
    Install & enable locally:

    ```
    pip install pre-commit
    pre-commit install
    pre-commit run --all-files
    ```
