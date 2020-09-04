from ansible_runner import Runner  # type: ignore
from logging import Logger
from openbsd_run.log import Log
from openbsd_run.config import Read as ReadConfig
from openbsd_run.playbook import path as playbook_path
from sys import exit
from typing import Any, Dict

import click
import ansible_runner as ansible


@click.command(short_help="Patch host(s) using syspatch")
@click.pass_context
def syspatch(context: Any) -> None:
    log: Logger = Log("openbsd-run: syspatch")

    host_pattern = context.obj["host_pattern"]
    inventory = context.obj["inventory"]
    inventory_contents: Dict[Any, Any] = {}
    quiet: bool = context.obj["quiet"]
    verbose: bool = context.obj["verbose"]

    if not inventory:
        log.info("inventory not provided")
        exit(1)

    try:
        inventory_contents = ReadConfig(inventory)
    except FileNotFoundError:
        log.error("file '%s' does not exist" % inventory)
        exit(1)
    except NotADirectoryError:
        log.error("'%s' is not a file" % inventory)
        exit(1)

    if not inventory_contents:
        log.error("inventory is invalid:", inventory_contents)
        exit(1)

    result: Runner = ansible.run(
        inventory=inventory_contents,
        limit=host_pattern,
        playbook="%s/site-syspatch.yml" % playbook_path,
        project_dir=playbook_path,
        roles_path="%s/roles" % playbook_path,
        quiet=quiet,
        suppress_ansible_output=True,
        verbosity="3" if verbose else None,
    )

    if result.rc != 0 or result.errored or result.canceled:
        log.error("update failed!")
        exit(1)
