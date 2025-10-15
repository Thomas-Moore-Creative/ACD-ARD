Contributing quick-guide

- Branch naming: `feat/...`, `fix/...`, `ci/...`.
- Commit messages: short summary line (<=72 chars) and optional body. Reference issue IDs when relevant.
- Pre-PR checklist:
  - Run `ruff check --fix .` and `black .` locally.
  - Run unit tests: `pytest -q`.
  - Update docs/instructions if behaviour or data layout changes.
- PR review:
  - Keep PRs focussed and small when possible.
  - Provide context in PR description (what changed, why, how to test).

- Developers: add yourself to CODEOWNERS if you maintain specific modules.