# CI instructions — Minimal & Extendable

Goals

- Keep CI minimal and reliable: fail fast on real issues (tests, import errors).
- Provide clear hooks and comments so the CI can be safely extended later (linting, typing, artifact uploads).

What CI must do (bare minimum)

1. Checkout the repo and set up a supported Python version (3.11).
2. Install package in editable mode plus test runtime deps: `pip install -e .[dev]` (or `pip install -e . pytest pytest-cov`).
3. Run a small, fast smoke test that verifies core imports and CLI entry points.
   - Example: `pytest -q tests/test_min_smoke.py --junitxml=pytest.xml --cov=src --cov-report=xml:coverage.xml`
4. Exit non-zero on any failure so PRs block on real regressions.

Recommended minimal GitHub Actions workflow (example)

- name: CI
  on: [push, pull_request]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Setup Python
          uses: actions/setup-python@v5
          with:
            python-version: '3.11'
        - name: Install deps
          run: |
            python -m pip install --upgrade pip
            pip install -e .[dev]
        - name: Run smoke tests
          run: |
            pytest -q tests/test_min_smoke.py --junitxml=pytest.xml --cov=src --cov-report=xml:coverage.xml
        - name: Upload artifacts
          if: always()
          uses: actions/upload-artifact@v4
          with:
            name: pytest-artifacts
            path: |
              pytest.xml
              coverage.xml

Breadcrumbs for later improvements

- Linting: add a `ruff check .` step (make it a separate job). Do not `continue-on-error` in the long term — treat linting as quality gate. For initial rollout, run linting in a separate job with `allow-failure` until rules are cleaned up.

- Formatting: run `black --check .` in CI (not `black .` to avoid modifying repo in the runner).

- Type checking: add `mypy` after ensuring `packages` points to the correct package name in `pyproject.toml`.

- Caching: add `actions/cache` for pip cache to speed up repeated runs.

- Test matrix: later expand to multiple Python versions using a matrix.

- Conditional steps: run slow or integration tests only on `workflow_dispatch` or a dedicated job to avoid wasting CI minutes on every push.

Notes and rationale

- Keep the first iteration tiny and stable. The core purpose is to catch regressions in imports, packaging, and the smallest smoke tests before merge.
- Use artifacts (junit/coverage) from the start — they help diagnose failures without making linting mandatory.
- Document every added CI step in `instructions/ci.instructions.md` so reviewers know why a step exists.

What's next if you approve

- I can update `.github/workflows/ci.yml` to the minimal workflow above and adjust `pyproject.toml` only if you want (e.g., ensure dev extras include pytest and ruff). I will not enable lint failing until you confirm.

Finished: draft ready for approval.