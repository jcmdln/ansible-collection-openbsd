from logging import (
    DEBUG,
    FileHandler,
    Formatter,
    Logger,
    StreamHandler,
    getLogger,
)


def Log(title: str) -> Logger:
    log: Logger = getLogger("openbsd-run: {}".format(title))

    logfile: str = ""
    try:
        with open("/var/log/openbsd-run.log", "w+") as fd:
            fd.close()
        logfile = "/var/log/openbsd-run.log"
    except Exception:
        logfile = "openbsd-run.log"

    log.propagate = False
    log.setLevel(DEBUG)
    f = Formatter(
        "%(asctime)s %(name)s: %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not log.hasHandlers():
        # Add a log handler for printing to stdout and stderr
        sh = StreamHandler()
        sh.setFormatter(f)
        log.addHandler(sh)

        # Add a log handler for logging to a file
        fh = FileHandler(logfile)
        fh.setFormatter(f)
        log.addHandler(fh)

    return log
