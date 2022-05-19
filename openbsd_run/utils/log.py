# SPDX-License-Identifier: ISC

from logging import DEBUG, FileHandler, Formatter, Logger, StreamHandler, getLogger


def Log(title: str) -> Logger:
    log: Logger = getLogger("{}".format(title))

    logfile: str = ""
    try:
        with open("/var/log/openbsd-run.log", "a") as fd:
            fd.close()
        logfile = "/var/log/openbsd-run.log"
    except Exception:
        # If we hit any exception, we won't log to a file
        logfile = ""
        pass

    log.propagate = False
    log.setLevel(DEBUG)

    if not log.hasHandlers():
        sh = StreamHandler()
        sh.setFormatter(Formatter("%(name)s: %(levelname)s: %(message)s"))
        log.addHandler(sh)

        if logfile:
            fh = FileHandler(logfile)
            fh.setFormatter(
                Formatter(
                    "%(asctime)s %(name)s: %(levelname)s: %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                )
            )
            log.addHandler(fh)

    return log
