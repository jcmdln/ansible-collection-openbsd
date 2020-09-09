#!/usr/bin/env python

from __future__ import absolute_import
from ansible.module_utils.basic import AnsibleModule  # type: ignore
from typing import Any, Dict


class Signify:
    def __init__(self, module: AnsibleModule) -> None:
        """
        """
        self.module: AnsibleModule = module

        self.changed: bool = False
        self.command: str = "/usr/sbin/signify"
        self.msg: str = ""
        self.rc: int = 0
        self.reboot: bool = False
        self.stdout: str = ""
        self.stderr: str = ""


def main() -> None:
    module: AnsibleModule = AnsibleModule(argument_spec={})

    signify: Signify = Signify(module)

    result: Dict[str, Any] = {
        "changed": signify.changed,
        "command": signify.command,
        "msg": signify.msg,
        "reboot": signify.reboot,
        "rc": signify.rc,
        "stdout": signify.stdout,
        "stderr": signify.stderr,
    }

    if signify.rc > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == "__main__":
    main()
