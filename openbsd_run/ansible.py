import ansible_runner as ansible


class Config(ansible.RunnerConfig):  # type: ignore
    """
    """

    def Play(self) -> tuple:
        """
        """
        return ansible.Runner.run(config=self.config)


if __name__ == "__main__":
    config: Config = Config()
    print(Play(config))
