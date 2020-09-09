from openbsd_run.cmd.pkg_add import pkg_add
from openbsd_run.cmd.pkg_delete import pkg_delete
from openbsd_run.cmd.syspatch import syspatch
from openbsd_run.cmd.sysupgrade import sysupgrade
from typing import List

__all__: List[str] = ["pkg_add", "pkg_delete", "syspatch", "sysupgrade"]
