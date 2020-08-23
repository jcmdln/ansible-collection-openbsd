from openbsd_run.playbook import path as playbook_path
from typing import Any, Dict
import ansible_runner as ansible
import click
import yaml
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

    inventory_contents: Dict[Any, Any] = {}

    if not inventory:
        print("openbsd-run: error: inventory not provided")
        sys.exit(1)

    with open(inventory, "r") as f:
        inventory_contents = yaml.safe_load(f.read())

    if not inventory_contents:
        print("openbsd-run: error: inventory is invalid:", inventory_contents)
        sys.exit(1)

    if update:
        result = ansible.run(
            host_pattern=host_pattern,
            inventory=inventory_contents,
            playbook="%s/site-update.yml" % playbook_path,
            private_data_dir="/tmp/openbsd-run",
            project_dir=playbook_path,
            roles_path="%s/roles" % playbook_path,
            quiet=quiet,
        )

        if result.errored:
            print("openbsd-run: error: update failed!")
            sys.exit(1)

        if result.stats["changed"]:
            print("openbsd-run: update completed successfully")
        else:
            print("openbsd-run: no newer updates available")

        sys.exit(0)


if __name__ == "__main__":
    main()
