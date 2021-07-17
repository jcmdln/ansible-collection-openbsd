# SPDX-License-Identifier: ISC

from __future__ import annotations

from ansible.module_utils.basic import AnsibleModule


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

    result: dict[str, bool | int | str] = {
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

    module.exit_json(**result)


if __name__ == "__main__":
    main()
