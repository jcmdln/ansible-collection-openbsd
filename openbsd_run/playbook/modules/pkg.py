#!/usr/bin/python

from __future__ import absolute_import
from ansible.module_utils.basic import AnsibleModule
from typing import Any, Dict, List
import re


class Pkg:
    def __init__(self, module: AnsibleModule) -> None:
        self.module: AnsibleModule = module
        self.packages: Dict[str, Any] = {}
        self.packages_raw: List[str] = []

        self.changed: bool = False
        self.command: str = ""
        self.msg: str = "no action performed"
        self.rc: int = 0
        self.stdout: str = ""
        self.stderr: str = ""

    def Add(self) -> None:
        """
        Add or update package(s)
        """

        self.command = "/usr/sbin/pkg_add -Ivx"
        pkgs: List[str] = self.module.params["name"]
        new_pkgs: List[str] = list(
            set(pkgs) - set(self.packages_raw) - set(self.packages.keys())
        )

        if self.module.params["state"] == "latest":
            pkg_action = "updated"
            __command = "{} -u".format(self.command)
            if "*" not in self.module.params["name"]:
                for p in [p for p in self.packages.keys() if p in pkgs]:
                    __command = "{} {}".format(self.command, p)

            self.rc, self.stdout, self.stderr = self.module.run_command(
                __command, check_rc=False, use_unsafe_shell=True
            )
        else:
            pkg_action = "installed"

        if new_pkgs and "*" not in self.module.params["name"]:
            for p in new_pkgs:
                self.command = "{} {}".format(self.command, p)

            self.rc, self.stdout, self.stderr = self.module.run_command(
                self.command, check_rc=False
            )

        if self.rc != 0:
            self.msg = "received a non-zero exit code"
            return

        if len(self.stdout) <= 2:
            self.command = ""
            return

        self.changed = True
        self.msg = "packages {}".format(pkg_action)

    def Delete(self) -> None:
        """
        Delete installed package(s)
        """

        self.command = "/usr/sbin/pkg_delete -Ivx"
        to_delete: Dict[str, Any] = {}

        if "*" in self.module.params["name"]:
            self.command = ""
            self.msg = "refusing to attempt removing all packages"
            self.rc = 1
            return

        for pkg in self.packages:
            if pkg in self.module.params["name"]:
                to_delete[pkg] = ""

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
        """
        Collect information about currently installed packages
        """

        self.command = "/usr/sbin/pkg_info -q"
        self.rc, stdout, stderr = self.module.run_command(
            self.command, check_rc=False
        )

        pkgs = stdout.split("\n")
        for pkg in pkgs:
            if not pkg:
                continue
            name = re.sub(r"-[0-9].*$", "", pkg)
            vers = re.search(r"-([\d.]+.*$)", pkg).group(1)  # type: ignore
            self.packages[name] = {"version": "{}".format(vers)}
            self.packages_raw.append(pkg)


def main() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec={
            "name": {"elements": "str", "type": "list"},
            "state": {
                "choices": ["absent", "latest", "present"],
                "required": True,
                "type": "str",
            },
        },
        mutually_exclusive=[["list", "name"], ["list", "state"]],
        required_one_of=[["list", "name"]],
        supports_check_mode=True,
    )

    pkg: Pkg = Pkg(module)

    pkg.Info()

    if module.params["state"] == "absent":
        pkg.Delete()
    elif module.params["state"] in ["latest", "present"]:
        pkg.Add()

    # Convert specific properties to a dict so we return specific data
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
