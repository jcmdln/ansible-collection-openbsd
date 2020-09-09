from ansible_runner import Runner  # type: ignore
from logging import Logger
from openbsd_run.log import Log
from openbsd_run.playbook import path as playbook_path
from sys import exit
from typing import Any, Dict

import click
import ansible_runner as ansible


@click.command(short_help="Upgrade host(s) using sysupgrade")
@click.option(
    "-f",
    default=False,
    help="Force an already applied upgrade",
    is_flag=True,
    type=bool,
)
@click.option(
    "-n",
    default=False,
    help="Fetch, verify, and create /bsd.upgrade but do not reboot",
    is_flag=True,
    type=bool,
)
@click.option(
    "-r",
    default=False,
    help="Upgrade to next release",
    is_flag=True,
    type=bool,
)
@click.option(
    "-s",
    default=False,
    help="Upgrade to next snapshot",
    is_flag=True,
    type=bool,
)
@click.pass_context
def sysupgrade(context: Any, f: bool, n: bool, r: bool, s: bool) -> None:
    log: Logger = Log("openbsd-run: sysupgrade")

    host_pattern = context.obj["host_pattern"]
    inventory_contents: Dict[Any, Any] = context.obj["inventory_contents"]
    quiet: bool = context.obj["quiet"]
    verbose: bool = context.obj["verbose"]

    extra_vars: Dict[str, Any] = {}

    if f:
        extra_vars["sysupgrade_force"] = True

    if n:
        extra_vars["sysupgrade_reboot"] = False

    if r:
        extra_vars["sysupgrade_branch"] = "release"
    elif s:
        extra_vars["sysupgrade_branch"] = "snapshot"

    result: Runner = ansible.run(
        extravars=extra_vars,
        inventory=inventory_contents,
        limit=host_pattern,
        playbook="%s/site-sysupgrade.yml" % playbook_path,
        project_dir=playbook_path,
        quiet=quiet,
        suppress_ansible_output=True,
        verbosity="3" if verbose else None,
    )

    if result.rc != 0 or result.errored or result.canceled:
        log.error("update failed!")
        exit(1)
