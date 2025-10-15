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


## Repository checklist (future work)

The repo currently has a minimal contribution guide in this `instructions/` directory, but a few repository-level artifacts are missing and should be added later to make contributions smoother:

- Add `CONTRIBUTING.md` in the project root (summarise this file and link to `instructions/`).
- Add `CODE_OF_CONDUCT.md` (e.g. Contributor Covenant) to set expectations.
- Add simple templates under `.github/` for issues and PRs (`.github/PULL_REQUEST_TEMPLATE.md`, `.github/ISSUE_TEMPLATE/`).
- Add `.pre-commit-config.yaml` to run `ruff`/`black` locally before commits.
- Optional: add `CODEOWNERS` to nominate maintainers for key paths.

Priority: `CONTRIBUTING.md` + `.pre-commit-config.yaml` are the highest-value small wins; the others are nice-to-have.

If you'd like, I can create these starter files in a follow-up PR — just tell me which ones to add.