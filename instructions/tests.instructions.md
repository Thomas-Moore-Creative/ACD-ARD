# Testing guidelines

## Unit tests

- Keep unit tests focused and fast.
- Use `pytest` fixtures (`tmp_path`, `monkeypatch`) to avoid touching disk/system state.

## Integration tests

- Tag slow or HPC tests with markers (`@pytest.mark.slow`, `@pytest.mark.hpc`) and exclude them from default CI.
- Use small sample datasets committed to `tests/data` or generated on-the-fly.

## Coverage

- Use `pytest-cov` to collect coverage and produce reports for the team.
- Aim for meaningful coverage; prioritize tests for data-loading and critical transforms.

## Running tests locally

- `pytest -q` for quick runs
- `pytest -q -m 'not slow'` to exclude slow tests

## Test data

- Prefer synthetic small datasets over large real data in tests.
- Document how to regenerate or extend test fixtures.