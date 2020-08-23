import click


@click.command(
    name="openbsd-run",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(None, "-v", "--version")
@click.option("--quiet", "-q", default=False, help="Suppress Ansible output")
@click.option(
    "--update", "-u", default=False, help="Upgrade, patch and update packages"
)
def main(quiet: bool, update: bool) -> None:
    """
    """


if __name__ == "__main__":
    main()
