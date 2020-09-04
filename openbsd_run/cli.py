from openbsd_run.cmd import syspatch, sysupgrade
from typing import Any

import click


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--host_pattern",
    "-H",
    type=str,
    default="",
    help="Host pattern to match against inventory",
)
@click.option(
    "--inventory", "-i", default="", help="Inventory file", type=str,
)
@click.option(
    "--quiet",
    "-q",
    default=False,
    help="Suppress Ansible output",
    is_flag=True,
    type=bool,
)
@click.option(
    "--verbose",
    "-V",
    default=False,
    help="Increase Ansible output",
    is_flag=True,
    type=bool,
)
@click.pass_context
@click.version_option(None, "-v", "--version")
def cli(
    context: Any, host_pattern: str, inventory: str, quiet: bool, verbose: bool
) -> None:
    context.ensure_object(dict)
    context.obj["host_pattern"] = host_pattern
    context.obj["inventory"] = inventory
    context.obj["quiet"] = quiet
    context.obj["verbose"] = verbose
    pass


if __name__ == "__main__":
    cli(obj={})

cli.add_command(syspatch)
cli.add_command(sysupgrade)
