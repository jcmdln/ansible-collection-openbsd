#!/usr/bin/env python

from __future__ import absolute_import
from ansible.module_utils.basic import AnsibleModule  # type: ignore
from typing import Any, Dict, List
import re


class Pkg:
    def __init__(self, module: AnsibleModule) -> None:
        self.module: AnsibleModule = module
        self.packages: Dict[str, Any] = {}

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

        pkgs: List[str] = self.module.params["name"]
        to_update: Dict[str, None] = {}

        if self.module.params["force"] and self.module.params["force"] not in [
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
            self.msg = (
                "'%s' is not a valid choice when adding packages"
                % self.module.params["force"]
            )
            self.rc = 1
            return

        if self.module.params["force"]:
            self.command = "%s -D %s" % (
                self.command,
                self.module.params["force"],
            )

        for pkg in self.packages:
            package = self.packages[pkg]["name"]
            if pkg in pkgs or package in pkgs:
                to_update[package] = None
                pkgs = list(set(pkgs) - set([pkg]) - set([package]))

        if self.module.params["state"] == "latest":
            if to_update or "*" in self.module.params["name"]:
                __latest_cmd = "{} -u".format(self.command)

            if "*" not in self.module.params["name"]:
                for p in to_update.keys():
                    __latest_cmd = "%s %s" % (__latest_cmd, p)

        if pkgs and "*" not in self.module.params["name"]:
            __present_cmd = "{} -v".format(self.command)
            for p in pkgs:
                __present_cmd = "%s %s" % (__present_cmd, p)

        if __latest_cmd or (pkgs and __present_cmd):
            if __latest_cmd and __present_cmd:
                self.command = "%s && %s" % (__latest_cmd, __present_cmd)
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
        to_delete: Dict[str, None] = {}

        if self.module.params["force"] and self.module.params["force"] not in [
            "baddepend",
            "checksum",
            "dependencies",
            "nonroot",
            "scripts",
        ]:
            self.command = ""
            self.msg = (
                "'%s' is not a valid choice when deleting packages"
                % self.module.params["force"]
            )
            self.rc = 1
            return

        if self.module.params["force"]:
            self.command = "%s -D %s" % (
                self.command,
                self.module.params["force"],
            )

        if "*" in self.module.params["name"]:
            self.command = ""
            self.msg = "refusing to attempt removing all packages"
            self.rc = 1
            return

        for pkg in self.packages:
            package = self.packages[pkg]["name"]
            if pkg in self.module.params["name"]:
                to_delete[pkg] = None
            elif package in self.module.params["name"]:
                to_delete[package] = None

        if not to_delete:
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
            version = re.search(r"-([\d.]+.*$)", pkg).group(1)  # type: ignore
            self.packages[pkg] = {"name": name, "version": "%s" % version}


def main() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec={
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
                "required": False,
                "type": "str",
            },
            "name": {"elements": "str", "type": "list"},
            "state": {
                "choices": ["absent", "latest", "present"],
                "required": True,
                "type": "str",
            },
        },
        mutually_exclusive=[["list", "name"], ["list", "state"]],
        required_one_of=[["list", "name"]],
        supports_check_mode=False,
    )

    pkg: Pkg = Pkg(module)

    pkg.Info()

    if module.params["state"] == "absent":
        pkg.Delete()
    elif module.params["state"] in ["latest", "present"]:
        pkg.Add()

    result: Dict[str, Any] = {
        "changed": pkg.changed,
        "command": pkg.command,
        "msg": pkg.msg,
        "rc": pkg.rc,
        "stdout": pkg.stdout,
        "stderr": pkg.stderr,
    }

    if pkg.rc > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == "__main__":
    main()
