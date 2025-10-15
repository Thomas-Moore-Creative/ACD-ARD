# Shell / Bash guidance
Shell / Bash guidance

- Use at top of scripts:
  - `#!/usr/bin/env bash` (or `#!/bin/sh` for POSIX scripts)
  - `set -euo pipefail` to fail fast on errors and unset variables.
- Prefer POSIX-compatible constructs unless you explicitly require Bash features.
- Print actions before destructive operations and require explicit confirmation (e.g. `--yes` flag).
- For dangerous operations (rm -rf) list targets first and require `--confirm` / `--yes` before executing.
- Use `mktemp` for temporary files and `trap` to clean them up on exit.
- Prefer `printf` over `echo -n` for portability.
- Check return codes for subshells and long pipelines; use `||`/`&&` as needed.
- Log actions and errors to a file for CI debugging; use `exec > >(tee -a "$LOG") 2>&1` when appropriate.
- Avoid parsing ls output; use `find` and `xargs -0` for safe file handling.
- When writing scripts that will run on clusters, make resource requirements explicit and document expected runtime and memory.

Small example (safe deletion pattern):
