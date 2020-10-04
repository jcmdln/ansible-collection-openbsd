from ansible_runner import Runner  # type: ignore
from logging import Logger
from openbsd_run.log import Log
from openbsd_run.playbook import path as playbook_path
from sys import exit
from typing import Any, Dict, List

import click
import ansible_runner as ansible


@click.command(short_help="Remove packages")
@click.option(
    "-D",
    default="",
    help="Force package removal, waiving the specified failsafe",
    type=str,
)
@click.argument("packages", required=True)
@click.pass_context
def pkg_delete(context: Any, d: str, packages: List[str]) -> None:
    log: Logger = Log("openbsd-run: pkg")

    host_pattern = context.obj["host_pattern"]
    inventory_contents: Dict[Any, Any] = context.obj["inventory_contents"]
    quiet: bool = context.obj["quiet"]
    verbose: bool = context.obj["verbose"]

    extra_vars: Dict[Any, Any] = {}

    if not packages or "*" in packages:
        log.error("'%s' is not a valid list of package names" % packages)
        exit(1)
    else:
        extra_vars["pkg_packages"] = packages
        extra_vars["pkg_state"] = "absent"

    if d and d not in [
        "baddepend",
        "checksum",
        "dependencies",
        "nonroot",
        "scripts",
    ]:
        log.error("'%s' is not a valid failsafe to waive.")
        exit(1)

    if d:
        extra_vars["pkg_force"] = d

    result: Runner = ansible.run(
        extravars=extra_vars,
        inventory=inventory_contents,
        limit=host_pattern,
        playbook="%s/site-pkg.yml" % playbook_path,
        project_dir=playbook_path,
        quiet=quiet,
        suppress_ansible_output=True,
        verbosity=3 if verbose else None,
    )

    if result.rc != 0 or result.errored or result.canceled:
        log.error("update failed!")
        exit(1)
