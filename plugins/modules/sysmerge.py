# SPDX-License-Identifier: ISC
#
# Copyright (c) 2023 Johnathan C. Maudlin <jcmdln@gmail.com>

from __future__ import annotations

from ansible.module_utils.basic import AnsibleModule


class Sysmerge:
    def __init__(self, module: AnsibleModule) -> None:
        self.module: AnsibleModule = module

        # Module parameters

        # Return values
        self.changed: bool = False
        self.command: str = ""
        self.msg: str = "no action required"
        self.rc: int = 0
        self.stdout: str = ""
        self.stderr: str = ""


def main() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec={},
        supports_check_mode=False,
    )

    sysmerge: Sysmerge = Sysmerge(module)

    result: dict[str, bool | int | str] = {
        "changed": sysmerge.changed,
        "command": sysmerge.command,
        "msg": sysmerge.msg,
        "rc": sysmerge.rc,
        "stdout": sysmerge.stdout,
        "stderr": sysmerge.stderr,
    }

    if sysmerge.rc > 0:
        module.fail_json(**result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
