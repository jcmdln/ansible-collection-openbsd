from logging import Logger
from openbsd_run.cmd import pkg_add, pkg_delete, syspatch, sysupgrade
from openbsd_run.config import Read as ReadConfig
from openbsd_run.log import Log
from typing import Any, Dict

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
    log: Logger = Log("openbsd-run")

    context.ensure_object(dict)
    context.obj["host_pattern"] = host_pattern
    context.obj["inventory"] = inventory
    context.obj["quiet"] = quiet
    context.obj["verbose"] = verbose

    if not inventory:
        log.info("inventory not provided")
        exit(1)

    try:
        inventory_contents: Dict[Any, Any] = ReadConfig(inventory)
        context.obj["inventory_contents"] = inventory_contents
    except FileNotFoundError:
        log.error("file '%s' does not exist" % inventory)
        exit(1)
    except NotADirectoryError:
        log.error("'%s' is not a file" % inventory)
        exit(1)

    if not inventory_contents:
        log.error("inventory is invalid:", inventory_contents)
        exit(1)

    pass


if __name__ == "__main__":
    cli(obj={})

cli.add_command(pkg_add)
cli.add_command(pkg_delete)
cli.add_command(syspatch)
cli.add_command(sysupgrade)
