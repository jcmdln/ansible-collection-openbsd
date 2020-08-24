#!/usr/bin/python

from __future__ import absolute_import
from ansible.module_utils.basic import AnsibleModule
from typing import Any, Dict, List


class Pkg:
    def __init__(self, module: AnsibleModule) -> None:
        self.module: AnsibleModule = module

        self.changed: bool = False
        self.command: str = ""
        self.msg: str = ""
        self.rc: int = 0
        self.stdout: str = ""
        self.stderr: str = ""

        self.host_packages: List[str] = []

    def Add(self, packages: List[str]) -> None:
        """
        """

        package_action: str = "installed"
        self.command = "/usr/sbin/pkg_add"

        if self.module.params["state"] == "latest":
            package_action = "updated"
            self.command = "{} -u".format(self.command)

        if self.module.params["name"] and self.module.params["name"] != "*":
            for package in self.module.params["name"]:
                self.command = "{} {}".format(self.command, package)

        self.rc, self.stdout, self.stderr = self.module.run_command(
            self.command, check_rc=False
        )

        if self.rc != 0:
            self.msg = "received a non-zero exit code"
            return

        if len(self.stdout.split("\n")) <= 2:
            self.msg = "no action performed"
            return

        self.changed = True
        self.msg = "packages {}".format(package_action)

    def Delete(self, packages: List[str]) -> None:
        """
        """

        package_action: str = "removed"
        self.command = "/usr/sbin/pkg_delete"

        if self.module.params["name"] == "*":
            self.command = "{} -a".format(self.command)
        else:
            for package in self.module.params["name"]:
                self.command = "{} {}".format(self.command, package)

        self.rc, self.stdout, self.stderr = self.module.run_command(
            self.command, check_rc=False
        )

        if self.rc != 0:
            self.msg = "received a non-zero exit code"
            return

        if len(self.stdout.split("\n")) <= 2:
            self.msg = "no action performed"
            return

        self.changed = True
        self.msg = "packages {}".format(package_action)

    def Info(self) -> List[str]:
        """
        """

        self.command = "/usr/sbin/pkg_info -q"
        self.rc, self.stdout, self.stderr = self.module.run_command(
            self.command, check_rc=False
        )

        self.host_packages = self.stdout.split("\n")

        if self.module.params["name"] and self.module.params["name"] != "*":
            for package in self.module.params["name"]:
                self.command = "{} -I inst:{}".format(self.command, package)

            self.rc, self.stdout, self.stderr = self.module.run_command(
                self.command, check_rc=False
            )

        return self.stdout.split("\n")


def main() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec={
            "list": {"type": "bool"},
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

    if module.params["state"] in ["absent", "present"]:
        pkg_list: List[str] = pkg.Info()

    if module.params["state"] == "absent":
        to_del: List[str] = list(set(module.params["name"]) - set(pkg_list))
        if to_del:
            pkg.Delete(to_del)
    elif module.params["state"] == "present":
        to_add: List[str] = list(set(pkg_list) - set(module.params["name"]))
        if to_add:
            pkg.Add(to_add)
    elif module.params["name"] and module.params["state"] == "latest":
        pkg.Add(module.params["name"])

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
