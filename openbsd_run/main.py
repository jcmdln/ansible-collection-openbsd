import click


@click.command(
    name="openbsd-run",
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.version_option(None, "-v", "--version")
def main() -> None:
    """
    """


if __name__ == "__main__":
    main()
