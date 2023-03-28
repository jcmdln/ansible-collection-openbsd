# SPDX-License-Identifier: ISC
#
# Copyright (c) 2023 Johnathan C. Maudlin <jcmdln@gmail.com>

from __future__ import annotations

from ansible.module_utils.basic import AnsibleModule


class Rcctl:
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

    rcctl: Rcctl = Rcctl(module)

    result: dict[str, bool | int | str] = {
        "changed": rcctl.changed,
        "command": rcctl.command,
        "msg": rcctl.msg,
        "rc": rcctl.rc,
        "stdout": rcctl.stdout,
        "stderr": rcctl.stderr,
    }

    if rcctl.rc > 0:
        module.fail_json(**result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
