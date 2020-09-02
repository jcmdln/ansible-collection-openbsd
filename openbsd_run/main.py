from openbsd_run.config import Read as ReadConfig
from openbsd_run.log import Log
from openbsd_run.playbook import path as playbook_path

from ansible_runner import Runner  # type: ignore
from logging import Logger
from typing import Any, Dict

import ansible_runner as ansible
import click
import sys


@click.command(
    name="openbsd-run",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(None, "-v", "--version")
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
    "--update",
    "-u",
    default=False,
    help="Upgrade, patch and update packages",
    is_flag=True,
    type=bool,
)
def main(host_pattern: str, inventory: str, quiet: bool, update: bool) -> None:
    """
    """
    log: Logger = Log("openbsd-run: Main")

    inventory_contents: Dict[Any, Any] = {}
    tags: str = ""

    if not inventory:
        log.info("inventory not provided")
        sys.exit(1)

    try:
        inventory_contents = ReadConfig(inventory)
    except FileNotFoundError:
        log.error("file '%s' does not exist" % inventory)
        sys.exit(1)
    except NotADirectoryError:
        log.error("'%s' is not a file" % inventory)
        sys.exit(1)
    if not inventory_contents:
        log.error("inventory is invalid:", inventory_contents)
        sys.exit(1)

    if update:
        tags = "patch,upgrade"

    result: Runner = ansible.run(
        host_pattern=host_pattern,
        inventory=inventory_contents,
        playbook="%s/site.yml" % playbook_path,
        project_dir=playbook_path,
        roles_path="%s/roles" % playbook_path,
        quiet=quiet,
        suppress_ansible_output=True,
        tags=tags,
    )

    if result.rc != 0 or result.errored or result.canceled:
        log.error("update failed!")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
