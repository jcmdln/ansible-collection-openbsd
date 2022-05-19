# SPDX-License-Identifier: ISC

from __future__ import annotations

from ansible.module_utils.basic import AnsibleModule


class Sysupgrade:
    def __init__(self, module: AnsibleModule) -> None:
        """
        Upgrade a host to the latest release or snapshot.
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
        if self.module.params["branch"] == "release":
            self.command = "{} -r".format(self.command)
        elif self.module.params["branch"] == "snapshot":
            self.command = "{} -s".format(self.command)

        if self.module.params["force"]:
            self.command = "{} -f".format(self.command)

        self.rc, self.stdout, self.stderr = self.module.run_command(self.command, check_rc=False)

        if not self.stdout and not self.stderr:
            self.msg = "no actions performed"
            return

        if "already on latest" in self.stdout.lower():
            self.msg = self.stdout.split("\n")[-1].strip(".").lower()
            return

        if "404 not found" in self.stderr.lower():
            self.msg = "no newer {} available".format(self.module.params["branch"])
            self.rc = 0
            return

        if self.rc != 0 or "failed" in [
            self.stderr.lower(),
            self.stdout.lower(),
        ]:
            self.msg = "failed to upgrade host"
            self.rc = 1 if self.rc == 0 else self.rc
            return

        self.changed = True
        self.msg = "upgrade performed successfully"
        self.reboot = True


def main() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec={
            "branch": {
                "choices": ["auto", "release", "snapshot"],
                "required": True,
                "type": "str",
            },
            "force": {"default": False, "type": "bool"},
            "keep": {"default": False, "type": "bool"},
        },
        supports_check_mode=False,
    )

    sysupgrade: Sysupgrade = Sysupgrade(module)
    sysupgrade.Update()

    result: dict[str, bool | int | str] = {
        "changed": sysupgrade.changed,
        "command": sysupgrade.command,
        "msg": sysupgrade.msg,
        "reboot": sysupgrade.reboot,
        "rc": sysupgrade.rc,
        "stdout": sysupgrade.stdout,
        "stderr": sysupgrade.stderr,
    }

    if sysupgrade.rc > 0:
        module.fail_json(**result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
