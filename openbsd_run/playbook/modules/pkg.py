from __future__ import annotations

import re

from ansible.module_utils.basic import AnsibleModule


class Pkg:
    def __init__(self, module: AnsibleModule) -> None:
        self.module: AnsibleModule = module

        # Module parameters
        self.delete_unused: bool = module.params["delete_unused"]
        self.force: str = module.params["force"]
        self.name: list[str] = module.params["name"]
        self.replace_existing: bool = module.params["replace_existing"]
        self.state: str = module.params["state"]

        # Storage
        self.packages: dict = {}

        # Return values
        self.changed: bool = False
        self.command: str = ""
        self.msg: str = "no action required"
        self.rc: int = 0
        self.stdout: str = ""
        self.stderr: str = ""

    def Add(self) -> None:
        self.command = "/usr/sbin/pkg_add -I -x"
        __latest_cmd: str = ""
        __present_cmd: str = ""

        pkgs: list[str] = self.name
        to_update: dict[str, None] = {}

        if self.replace_existing:
            self.command = "{} -r".format(self.command)

        if self.force and self.force not in [
            "allversions",
            "arch",
            "checksum",
            "dontmerge",
            "donttie",
            "downgrade",
            "installed",
            "nonroot",
            "paranoid",
            "repair",
            "scripts",
            "SIGNER",
            "snap",
            "snapshot",
            "unassigned",
            "updatedepends",
        ]:
            self.command = ""
            self.msg = "'{}' is invalid when adding packages".format(
                self.force
            )
            self.rc = 1
            return

        if self.force:
            self.command = "{} -D {}".format(self.command, self.force)

        for pkg in self.packages:
            package = self.packages[pkg]["name"]
            if pkg in pkgs or package in pkgs:
                to_update[package] = None
                pkgs = list(set(pkgs) - set([pkg]) - set([package]))

        if self.state == "latest":
            if to_update or "*" in self.name:
                __latest_cmd = "{} -u".format(self.command)

            if "*" not in self.name:
                for p in to_update.keys():
                    __latest_cmd = "{} {}".format(__latest_cmd, p)

        if pkgs and "*" not in self.name:
            __present_cmd = "{} -v".format(self.command)
            for p in pkgs:
                __present_cmd = "{} {}".format(__present_cmd, p)

        if __latest_cmd or (pkgs and __present_cmd):
            if __latest_cmd and __present_cmd:
                self.command = "{} && {}".format(__latest_cmd, __present_cmd)
            elif __latest_cmd:
                self.command = __latest_cmd
            elif __present_cmd:
                self.command = __present_cmd

            self.rc, self.stdout, self.stderr = self.module.run_command(
                self.command, check_rc=False, use_unsafe_shell=True
            )

        if self.rc != 0 or self.stderr:
            self.changed = True
            self.msg = "received a non-zero exit code"
            self.rc = 1 if not self.rc else self.rc
            return

        if not self.stderr and len(self.stdout.splitlines()) <= 2:
            return

        self.changed = True
        self.msg = "completed successfully"

    def Delete(self) -> None:
        self.command = "/usr/sbin/pkg_delete -I -v -x"
        to_delete: dict[str, None] = {}

        if self.delete_unused:
            self.command = "{} -a".format(self.command)

        if self.force and self.force not in [
            "baddepend",
            "checksum",
            "dependencies",
            "nonroot",
            "scripts",
        ]:
            self.command = ""
            self.msg = "'{}' is invalid when deleting packages".format(
                self.force
            )
            self.rc = 1
            return

        if self.force:
            self.command = "{} -D {}".format(self.command, self.force)

        if "*" in self.name:
            self.command = ""
            self.msg = "refusing to attempt removing all packages"
            self.rc = 1
            return

        for pkg in self.packages:
            package = self.packages[pkg]["name"]
            if pkg in self.name:
                to_delete[pkg] = None
            elif package in self.name:
                to_delete[package] = None

        if not to_delete and not self.delete_unused:
            self.command = ""
            self.msg = "no action performed"
            return

        for package in to_delete:
            self.command = "{} {}".format(self.command, package)

        self.rc, self.stdout, self.stderr = self.module.run_command(
            self.command, check_rc=False
        )

        if self.rc != 0:
            self.msg = "received a non-zero exit code"
            return

        if self.delete_unused and "Deleting" not in self.stdout:
            self.msg = "no action performed"
            return

        self.changed = True
        self.msg = "packages removed successfully"

    def Info(self) -> None:
        self.command = "/usr/sbin/pkg_info -q"
        self.rc, stdout, stderr = self.module.run_command(
            self.command, check_rc=False
        )

        for pkg in stdout.splitlines():
            if not pkg:
                continue

            name = re.sub(r"-[0-9].*$", "", pkg)
            version = re.search(r"-([\d.]+.*$)", pkg)
            if version:
                version = version.group(1)

            self.packages[pkg] = {
                "name": name,
                "version": "{}".format(version),
            }


def main() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec={
            "delete_unused": {"default": False, "type": bool},
            "force": {
                "choices": [
                    "allversions",
                    "arch",
                    "baddepend",
                    "checksum",
                    "dependencies",
                    "dontmerge",
                    "donttie",
                    "downgrade",
                    "installed",
                    "nonroot",
                    "paranoid",
                    "repair",
                    "scripts",
                    "SIGNER",
                    "snap",
                    "snapshot",
                    "unassigned",
                    "updatedepends",
                ],
                "type": "str",
            },
            "name": {"elements": "str", "type": "list"},
            "replace_existing": {"default": False, "type": bool},
            "state": {
                "choices": ["absent", "latest", "present"],
                "required": True,
                "type": "str",
            },
        },
        supports_check_mode=False,
    )

    pkg: Pkg = Pkg(module)
    pkg.Info()

    if pkg.state == "absent":
        if not pkg.replace_existing:
            pkg.Delete()
        else:
            pkg.msg = "cannot mix 'replace_existing' with 'state: absent'"
            pkg.rc = 1
    elif pkg.state in ["latest", "present"]:
        if not pkg.delete_unused:
            pkg.Add()
        else:
            pkg.msg = "cannot mix 'delete' with 'state: {}'".format(pkg.state)
            pkg.rc = 1

    result: dict[str, bool | int | str] = {
        "changed": pkg.changed,
        "command": pkg.command,
        "msg": pkg.msg,
        "rc": pkg.rc,
        "stdout": pkg.stdout,
        "stderr": pkg.stderr,
    }

    if pkg.rc > 0:
        module.fail_json(**result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
