#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Johnathan C. Maudlin <jcmdln@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from ansible.module_utils.basic import AnsibleModule
from typing import Any, Dict


class Vmctl:
    def __init__(self, module: AnsibleModule) -> None:
        self.module: AnsibleModule = module

        self.changed: bool = False
        self.command: str = "/usr/sbin/vmctl"
        self.msg: str = ""
        self.rc: int = 0
        self.reboot: bool = False
        self.stdout: str = ""
        self.stderr: str = ""


def main() -> None:
    module: AnsibleModule = AnsibleModule(argument_spec={})

    vmctl: Vmctl = Vmctl(module)

    # Convert specific properties to a dict so we return specific data
    result: Dict[str, Any] = {
        "changed": vmctl.changed,
        "command": vmctl.command,
        "msg": vmctl.msg,
        "rc": vmctl.rc,
        "reboot": vmctl.reboot,
        "stdout": vmctl.stdout,
        "stderr": vmctl.stderr,
    }

    if vmctl.rc > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == "__main__":
    main()
