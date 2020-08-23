#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Johnathan C. Maudlin <jcmdln@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from ansible.module_utils.basic import AnsibleModule
from typing import Any, Dict

# https://man.openbsd.org/pfctl.8
# https://man.openbsd.org/pfsync.4


class Pfctl:
    def __init__(self, module: AnsibleModule) -> None:
        self.module: AnsibleModule = module

        self.changed: bool = False
        self.command: str = "/usr/sbin/pfctl"
        self.msg: str = ""
        self.rc: int = 0
        self.reboot: bool = False
        self.stdout: str = ""
        self.stderr: str = ""


def main() -> None:
    module: AnsibleModule = AnsibleModule(argument_spec={})

    pfctl: Pfctl = Pfctl(module)

    # Convert specific properties to a dict so we return specific data
    result: Dict[str, Any] = {
        "changed": pfctl.changed,
        "command": pfctl.command,
        "msg": pfctl.msg,
        "rc": pfctl.rc,
        "reboot": pfctl.reboot,
        "stdout": pfctl.stdout,
        "stderr": pfctl.stderr,
    }

    if pfctl.rc > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == "__main__":
    main()
