#!/usr/bin/env python

from __future__ import absolute_import, annotations

from ansible.module_utils.basic import AnsibleModule

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
    result: dict[str, bool | int | str] = {
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
