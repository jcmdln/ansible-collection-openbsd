import click


@click.command(
    name="openbsd-run",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(None, "-v", "--version")
@click.option("--update", "-u", default=False, help="")
def main(update: bool) -> None:
    """
    """


if __name__ == "__main__":
    main()
