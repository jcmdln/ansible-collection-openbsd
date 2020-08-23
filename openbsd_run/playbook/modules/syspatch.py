#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Johnathan C. Maudlin <jcmdln@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import
from ansible.module_utils.basic import AnsibleModule
from typing import Any, Dict


class Syspatch:
    def __init__(self, module: AnsibleModule) -> None:
        self.module: AnsibleModule = module

        self.changed: bool = False
        self.command: str = "/usr/sbin/syspatch"
        self.msg: str = ""
        self.rc: int = 0
        self.reboot: bool = False
        self.stdout: str = ""
        self.stderr: str = ""

    def Apply(self) -> None:
        """
        Apply all available patches
        """

        self.rc, self.stdout, self.stderr = self.module.run_command(
            self.command, check_rc=False
        )

        if self.rc != 0:
            self.msg = "received a non-zero exit code"
            return

        if not self.stdout and not self.stderr:
            self.msg = "no action performed"
            return

        if "reboot" in self.stdout:
            self.reboot = True

        self.changed = True
        self.msg = "patches applied"

    def List(self) -> None:
        """
        """
        if self.module.params["List"].lower() == "available":
            self.command = "%s -c" % (self.command)

        if self.module.params["List"].lower() == "installed":
            self.command = "%s -l" % (self.command)

        self.rc, self.stdout, self.stderr = self.module.run_command(
            self.command, check_rc=False
        )

        if self.rc != 0:
            self.msg = "received a non-zero exit code"
            return

        if not self.stdout and not self.stderr:
            self.msg = "no patches to list"
            return

        self.msg = "list of available patches returned"

    def Revert(self) -> None:
        """
        """
        if self.module.params["list"] == "all":
            self.command = "%s -R" % (self.command)

        if self.module.params["list"] == "latest":
            self.command = "%s -r" % (self.command)

        self.rc, self.stdout, self.stderr = self.module.run_command(
            self.command, check_rc=False
        )

        if self.rc != 0:
            self.msg = "received a non-zero exit code"
            return

        if not self.stdout and not self.stderr:
            self.msg = "no patches to revert"
            return

        if "reboot" in self.stdout.lower():
            self.reboot = True

        self.changed = True
        self.msg = "patches reverted"


def main() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec={
            "apply": {"type": "bool", "default": False},
            "list": {"type": "str", "choices": ["available", "installed"]},
            "revert": {"type": "str", "choices": ["all", "latest"]},
        },
        required_one_of=[["apply", "list", "revert"]],
        mutually_exclusive=[["apply", "list", "revert"]],
        supports_check_mode=False,
    )

    syspatch: Syspatch = Syspatch(module)

    if module.params["apply"]:
        syspatch.Apply()
    elif module.params["list"]:
        syspatch.List()
    elif module.params["revert"]:
        syspatch.Revert()

    # Convert specific properties to a dict so we return specific data
    result: Dict[str, Any] = {
        "changed": syspatch.changed,
        "command": syspatch.command,
        "msg": syspatch.msg,
        "rc": syspatch.rc,
        "reboot": syspatch.reboot,
        "stdout": syspatch.stdout,
        "stderr": syspatch.stderr,
    }

    if syspatch.rc > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == "__main__":
    main()
