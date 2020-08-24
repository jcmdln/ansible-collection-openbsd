#!/usr/bin/python

from __future__ import absolute_import
from ansible.module_utils.basic import AnsibleModule
from typing import Any, Dict


class Sysupgrade:
    def __init__(self, module: AnsibleModule) -> None:
        """
        """
        self.module: AnsibleModule = module

        self.changed: bool = False
        self.command: str = "/usr/sbin/sysupgrade -n"
        self.msg: str = ""
        self.rc: int = 0
        self.reboot: bool = False
        self.stdout: str = ""
        self.stderr: str = ""

    def Update(self) -> None:
        """
        """
        if self.module.params["branch"].lower() == "release":
            self.command = "%s -r" % (self.command)

        if self.module.params["branch"].lower() == "snapshot":
            self.command = "%s -s" % (self.command)

        self.rc, self.stdout, self.stderr = self.module.run_command(
            self.command, check_rc=False
        )

        if self.rc != 0:
            self.msg = "received a non-zero exit code"
            return

        if not self.stdout and not self.stderr:
            self.msg = "no actions performed"
            return

        if "Already on latest" in self.stdout:
            self.msg = self.stdout.split("\n")[-1].strip(".").lower()
            return

        if "Signature Verified" not in self.stdout:
            self.changed = True
            self.msg = "failed to verify downloaded files"
            self.rc = 1 if self.rc == 0 else self.rc
            return

        self.changed = True
        self.msg = "patches reverted"
        self.reboot = True


def main() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec={
            "branch": {
                "type": "str",
                "choices": ["auto", "release", "snapshot"],
                "default": "auto",
            },
            "force": {"type": "bool", "default": False},
        },
        supports_check_mode=True,
    )

    sysupgrade: Sysupgrade = Sysupgrade(module)

    # Convert specific properties to a dict so we return specific data
    result: Dict[str, Any] = {
        "changed": sysupgrade.changed,
        "command": sysupgrade.command,
        "msg": sysupgrade.msg,
        "rc": sysupgrade.rc,
        "stdout": sysupgrade.stdout,
        "stderr": sysupgrade.stderr,
    }

    if sysupgrade.rc > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == "__main__":
    main()
