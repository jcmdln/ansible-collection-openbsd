from ansible_runner import Runner  # type: ignore
from logging import Logger
from openbsd_run.log import Log
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
    inventory_contents: Dict[Any, Any] = context.obj["inventory_contents"]
    quiet: bool = context.obj["quiet"]
    verbose: bool = context.obj["verbose"]

    result: Runner = ansible.run(
        inventory=inventory_contents,
        limit=host_pattern,
        playbook="%s/site-syspatch.yml" % playbook_path,
        project_dir=playbook_path,
        quiet=quiet,
        suppress_ansible_output=True,
        verbosity="3" if verbose else None,
    )

    if result.rc != 0 or result.errored or result.canceled:
        log.error("update failed!")
        exit(1)
