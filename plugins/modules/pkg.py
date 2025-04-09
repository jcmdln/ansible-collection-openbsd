# SPDX-License-Identifier: ISC
#
# Copyright (c) 2023 Johnathan C. Maudlin <jcmdln@gmail.com>


from __future__ import absolute_import, annotations, division, print_function

__metaclass__ = type

import re

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
---
module: pkg
short_description: "Manage packages using pkg_* suite"
version_added: "1.2.0"

author: Johnathan Craig Maudlin (@jcmdln) <jcmdln@gmail.com>
description:
    - Manage packages using pkg_* suite

options:
    delete_unused:
        description:
            - Delete unused dependencies (packages that are not needed by anything tagged as installed manually).  Can be used without pkgnames.  If used with pkgnames, it will only delete non manual installs in the list.
        type: bool
        default: false

    force:
        description:
            - Force removal of the package by waiving a failsafe.
            - "When used with `state=absent`, only the following values are valid: `baddepend`, `checksum`, `dependencies`, `nonroot`, `scripts`"
            - "When used with `state=latest` or `state=present`, only the following values are valid: `allversions`, `arch`, `checksum` `dontmerge`, `donttie`, `downgrade`, `installed`, `nonroot` `repair`, `scripts` `SIGNER`, `snap`, `snapshot`, `unsigned`"
        type: str
        choices:
            - allversions
            - arch
            - baddepend
            - checksum
            - dependencies
            - dontmerge
            - donttie
            - downgrade
            - installed
            - nonroot
            - repair
            - scripts
            - SIGNER
            - snap
            - snapshot
            - unsigned

    name:
        description:
            - A package name or list of packages.
        type: list
        element: str
        default: []

    replace_existing:
        description:
            - thing
        type: bool
        default: false

    state:
        description:
            - thing
        type: str
        required: true
        choices:
            - absent
            - latest
            - present
"""

EXAMPLES = r"""
- name: Update all packages
  jcmdln.openbsd.pkg:
    name: "*"
    state: latest

- name: Install a package
  jcmdln.openbsd.pkg:
    name: cmake
    state: present

- name: Update existing packages and install missing packages
  jcmdln.openbsd.pkg:
    name:
      - cmake
      - nano
    state: latest

- name: Delete a package
  jcmdln.openbsd.pkg:
    name: cmake
    state: absent

- name: Delete existing packages
  jcmdln.openbsd.pkg:
    name:
      - cmake
      - nano
    state: absent
"""


class Pkg:
    # Results
    changed: bool = False
    command: str = ""
    msg: str = "no action required"
    rc: int = 0
    stdout: str = ""
    stderr: str = ""

    def __init__(self, module: AnsibleModule) -> None:
        self.module: AnsibleModule = module

    def add(self, *, force: str, name: list[str], replace_existing: bool, state: str) -> Pkg:
        self.command = "/usr/sbin/pkg_add -I -v -x"

        if force and force not in [
            "allversions",
            "arch",
            "checksum",
            "dontmerge",
            "donttie",
            "downgrade",
            "installed",
            "nonroot",
            "repair",
            "scripts",
            "SIGNER",
            "snap",
            "snapshot",
            "unsigned",
        ]:
            self.msg = f"'{force}' is invalid when adding packages"
            self.rc = 1
            return self

        if "*" in name and state == "present":
            self.msg = "Refusing to install all packages"
            self.rc = 1
            return self

        if self.module.check_mode:
            self.command = f"{self.command} -s"
        if force:
            self.command = f"{self.command} -D {force}".format()
        if replace_existing:
            self.command = f"{self.command} -r"

        # When updating all packages, skip all other package semantics.
        if "*" in name:
            self.command = f"{self.command} -u"
            self.rc, self.stdout, self.stderr = self.module.run_command(
                self.command, check_rc=False
            )
            self.changed = False if self.module.check_mode else "installing" in self.stdout
            self.msg = "Updated packages."
            return self

        # When ensuring packages are installed, skip all other package semantics.
        if state == "present":
            self.command = f"{self.command} {' '.join(name)}"
            self.rc, self.stdout, self.stderr = self.module.run_command(
                self.command, check_rc=False
            )
            self.changed = False if self.module.check_mode else "installing" in self.stdout
            self.msg = "Installed packages."
            return self

        # Collect the dict of currently installed packages.
        packages: dict = self.info()

        # Collect to_install packages, removing matches
        to_install: dict[str, None] = {}
        for pkg in [p for p in name if not packages.get(p)]:
            to_install[pkg] = None
            name = list(set(name) - {pkg})

        # Collect to_update packages, removing matches
        to_update: dict[str, None] = {}
        for pkg in name:
            to_update[pkg] = None
            name = list(set(name) - {pkg})

        cmd_install: str = f"{self.command} {' '.join(to_install.keys())}"
        print(cmd_install)
        cmd_update: str = f"{self.command} -u {' '.join(to_update.keys())}"
        print(cmd_update)
        if to_install and to_update:
            self.command = f"{cmd_update} && {cmd_install}"
            self.msg = "Updated and installed packages."
        elif to_install:
            self.command = cmd_install
            self.msg = "Installed packages."
        elif to_update:
            self.command = cmd_update
            self.msg = "Updated packages."

        self.rc, self.stdout, self.stderr = self.module.run_command(self.command, check_rc=False)
        self.changed = "installing" in self.stdout
        return self

    def delete(self, *, delete_unused: bool, force: str, name: list[str], state: str) -> Pkg:
        self.command = "/usr/sbin/pkg_delete -I -v -x"

        if force and force not in ["baddepend", "checksum", "dependencies", "nonroot", "scripts"]:
            self.command = ""
            self.msg = f"'{force}' is invalid when deleting packages"
            self.rc = 1
            return self
        if "*" in name and state == "present":
            self.msg = "Refusing to delete all packages"
            self.rc = 1
            return self

        if self.module.check_mode:
            self.command = f"{self.command} -s"
        if delete_unused:
            self.command = f"{self.command} -a"
        if force:
            self.command = f"{self.command} -D {force}".format()

        # When deleting all unused packages, skip all other package semantics.
        if not name and delete_unused:
            self.rc, self.stdout, self.stderr = self.module.run_command(
                self.command, check_rc=False
            )
            self.changed = False if self.module.check_mode else "Deleting" in self.stdout
            self.msg = "Deleted packages."
            return self

        # Collect the dict of currently installed packages.
        packages: dict = self.info()

        # Collect to_delete packages
        to_delete: dict[str, None] = {}
        for p in [p for p in packages if p in name or packages.get(p, {}).get("name") in name]:
            to_delete[p] = None
        if not to_delete:
            return self

        packages.values

        self.command = f"{self.command} {' '.join(to_delete.keys())}"
        self.rc, self.stdout, self.stderr = self.module.run_command(self.command, check_rc=False)
        self.changed = False if self.module.check_mode else "Deleting" in self.stdout
        self.msg = "Deleted packages."
        return self

    def info(self) -> dict:
        """Gather the name and version of all installed packages."""
        packages: dict = {}
        stdout: str

        _, stdout, _ = self.module.run_command("/usr/sbin/pkg_info -q", check_rc=False)
        for pkg in [pkg for pkg in stdout.splitlines() if pkg]:
            name = re.sub(r"-[0-9].*$", "", pkg)
            version: str = v.group(1) if (v := re.search(r"-([\d.]+.*$)", pkg)) else ""
            packages[pkg] = {"name": name, "version": f"{version}"}

        return packages


def main() -> None:
    module: AnsibleModule = AnsibleModule(
        argument_spec={
            "delete_unused": {"default": False, "type": bool},
            "force": {
                "choices": [
                    "checksum",
                    "nonroot",
                    "scripts",
                    # pkg_add only
                    "allversions",
                    "arch",
                    "dontmerge",
                    "donttie",
                    "downgrade",
                    "installed",
                    "repair",
                    "SIGNER",
                    "snap",
                    "snapshot",
                    "unsigned",
                    # pkg_delete only
                    "baddepend",
                    "dependencies",
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
        # required_one_of=[],
        supports_check_mode=True,
    )

    # Module arguments
    delete_unused: bool = module.params["delete_unused"]
    force: str = module.params["force"]
    name: list[str] = (
        module.params["name"]
        if isinstance(module.params["name"], list)
        else list(module.params["name"])
        if isinstance(module.params["name"], str)
        else []
    )
    replace_existing: bool = module.params["replace_existing"]
    state: str = module.params["state"]

    # Results
    pkg: Pkg = Pkg(module)

    # Determine which action(s) to perform
    if state == "absent":
        if replace_existing:
            pkg.msg = f"cannot mix 'delete_unused' with 'state: {state}'"
            pkg.rc = 1
        else:
            pkg.delete(
                delete_unused=delete_unused,
                force=force,
                name=name,
                state=state,
            )
    elif state in ["latest", "present"]:
        if delete_unused:
            pkg.msg = f"cannot mix 'delete_unused' with 'state: {state}'"
            pkg.rc = 1
        else:
            pkg.add(
                force=force,
                name=name,
                replace_existing=replace_existing,
                state=state,
            )

    result: dict = {
        "changed": pkg.changed,
        "command": pkg.command,
        "msg": pkg.msg,
        "rc": pkg.rc,
        "stdout": pkg.stdout,
        "stderr": pkg.stderr,
    }

    # Handle results
    if pkg.rc != 0:
        module.fail_json(**result)
    module.exit_json(**result)


if __name__ == "__main__":
    main()
