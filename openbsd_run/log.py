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

    if not log.hasHandlers():
        # fh = FileHandler("/var/log/openbsd-run.log")
        # fileFormat = Formatter(
        #     "%(asctime)s %(name)s: %(levelname)8s: %(message)s",
        #     datefmt="%Y-%m-%d %H:%M:%S",
        # )
        # fh.setFormatter(fileFormat)
        # log.addHandler(fh)

        sh = StreamHandler()
        streamFormat = Formatter("%(name)s: %(levelname)8s: %(message)s")
        sh.setFormatter(streamFormat)
        log.addHandler(sh)

    return log
