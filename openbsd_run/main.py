from openbsd_run.playbook import Path as playbook_path
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

    if not inventory:
        print("openbsd-run: error: inventory not provided")
        sys.exit(1)

    if update:
        result = ansible.run(
            artifact_dir="/tmp/openbsd-run",
            host_pattern=host_pattern,
            inventory=inventory,
            playbook="%s/site-update.yml" % playbook_path(),
            private_data_dir=playbook_path(),
            roles_path="%s/roles" % playbook_path(),
            quiet=quiet,
        )

        if result.errored:
            print("openbsd-run: error: update failed!")
            sys.exit(1)
        else:
            print("openbsd-run: update completed successfully")
            sys.exit(0)


if __name__ == "__main__":
    main()
