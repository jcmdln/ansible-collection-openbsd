from logging import (
    getLogger,
    # FileHandler,
    Formatter,
    Logger,
    StreamHandler,
    DEBUG,
)


def Log(function: str) -> Logger:
    log: Logger = getLogger("%s" % function)

    log.propagate = False
    log.setLevel(DEBUG)
    f = Formatter(
        "%(asctime)s %(name)s: %(levelname)8s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not log.hasHandlers():
        # fh = FileHandler("/var/log/openbsd-run.log")
        # fh.setFormatter(f)
        # log.addHandler(fh)

        sh = StreamHandler()
        sh.setFormatter(f)
        log.addHandler(sh)

    return log
