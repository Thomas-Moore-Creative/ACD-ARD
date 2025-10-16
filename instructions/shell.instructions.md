# Shell / Bash guidance
Shell / Bash guidance

- Print actions before destructive operations and require explicit confirmation (e.g. `--yes` flag).
- For dangerous operations (rm -rf) list targets first and require `--confirm` / `--yes` before executing.
- Use `mktemp` for temporary files and `trap` to clean them up on exit.
- Prefer `printf` over `echo -n` for portability.
- Log actions and errors to a file for debugging
- When writing scripts that will run on clusters, make resource requirements explicit and document expected runtime and memory.
