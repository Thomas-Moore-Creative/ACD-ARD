# CLI conventions (Click)

- One top-level Click group command (e.g. `acd-ard`) with short single-purpose subcommands.
- Provide `--help` and `--version` for all commands.
- Avoid long lists of positional args; prefer named options.
- For destructive actions provide `--yes` or `--confirm` flags and print planned actions before executing.
- Add unit tests for CLI commands using Click's `CliRunner`.

Example pattern:

```python
@click.group()
def cli():
    """Top level CLI."""
    pass

@cli.command()
@click.option("--yes", is_flag=True)
def delete(yes):
    if not yes:
        click.confirm("Are you sure?", abort=True)
    # perform action
