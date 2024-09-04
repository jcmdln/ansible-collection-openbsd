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


class Result:
    def __init__(
        self,
        changed: bool = False,
        command: str = "",
        msg: str = "no action required",
        rc: int = 0,
        stdout: str = "",
        stderr: str = "",
    ) -> None:
        self.changed: bool = changed
        self.command: str = command
        self.msg: str = msg
        self.rc: int = rc
        self.stdout: str = stdout
        self.stderr: str = stderr


def pkg_add(
    module: AnsibleModule,
    *,
    force: str,
    name: list[str],
    replace_existing: bool,
    state: str,
) -> Result:
    r: Result = Result()
    r.command = "/usr/sbin/pkg_add -I -v -x"

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
        r.msg = f"'{force}' is invalid when adding packages"
        r.rc = 1
        return r

    if "*" in name and state == "present":
        r.msg = "Refusing to install all packages"
        r.rc = 1
        return r

    if module.check_mode:
        r.command = f"{r.command} -s"
    if force:
        r.command = f"{r.command} -D {force}".format()
    if replace_existing:
        r.command = f"{r.command} -r"

    # When updating all packages, skip all other package semantics.
    if "*" in name:
        r.command = f"{r.command} -u"
        r.rc, r.stdout, r.stderr = module.run_command(r.command, check_rc=False)
        r.changed = False if module.check_mode else "installing" in r.stdout
        r.msg = "Updated packages."
        return r

    # When ensuring packages are installed, skip all other package semantics.
    if state == "present":
        r.command = f"{r.command} {' '.join(name)}"
        r.rc, r.stdout, r.stderr = module.run_command(r.command, check_rc=False)
        r.changed = False if module.check_mode else "installing" in r.stdout
        r.msg = "Installed packages."
        return r

    # Collect the dict of currently installed packages.
    packages: dict = pkg_info(module)

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

    cmd_install: str = f"{r.command} {' '.join(to_install.keys())}"
    print(cmd_install)
    cmd_update: str = f"{r.command} -u {' '.join(to_update.keys())}"
    print(cmd_update)
    if to_install and to_update:
        r.command = f"{cmd_update} && {cmd_install}"
        r.msg = "Updated and installed packages."
    elif to_install:
        r.command = cmd_install
        r.msg = "Installed packages."
    elif to_update:
        r.command = cmd_update
        r.msg = "Updated packages."

    r.rc, r.stdout, r.stderr = module.run_command(r.command, check_rc=False)
    r.changed = "installing" in r.stdout
    return r


def pkg_delete(
    module: AnsibleModule,
    *,
    delete_unused: bool,
    force: str,
    name: list[str],
    state: str,
) -> Result:
    r: Result = Result()
    r.command = "/usr/sbin/pkg_delete -I -v -x"

    if force and force not in ["baddepend", "checksum", "dependencies", "nonroot", "scripts"]:
        r.command = ""
        r.msg = f"'{force}' is invalid when deleting packages"
        r.rc = 1
        return r
    if "*" in name and state == "present":
        r.msg = "Refusing to delete all packages"
        r.rc = 1
        return r

    if module.check_mode:
        r.command = f"{r.command} -s"
    if delete_unused:
        r.command = f"{r.command} -a"
    if force:
        r.command = f"{r.command} -D {force}".format()

    # When deleting all unused packages, skip all other package semantics.
    if not name and delete_unused:
        r.rc, r.stdout, r.stderr = module.run_command(r.command, check_rc=False)
        r.changed = False if module.check_mode else "Deleting" in r.stdout
        r.msg = "Deleted packages."
        return r

    # Collect the dict of currently installed packages.
    packages: dict[str, dict] = pkg_info(module)

    # Collect to_delete packages
    to_delete: dict[str, None] = {}
    for p in [p for p in packages if p in name or packages.get(p, {}).get("name") in name]:
        to_delete[p] = None
    if not to_delete:
        return r

    packages.values

    r.command = f"{r.command} {' '.join(to_delete.keys())}"
    r.rc, r.stdout, r.stderr = module.run_command(r.command, check_rc=False)
    r.changed = False if module.check_mode else "Deleting" in r.stdout
    r.msg = "Deleted packages."
    return r


def pkg_info(module: AnsibleModule) -> dict:
    """Gather the name and version of all installed packages."""
    packages: dict = {}
    stdout: str

    _, stdout, _ = module.run_command("/usr/sbin/pkg_info -q", check_rc=False)
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
    result: Result = Result()

    # Determine which action(s) to perform
    if state == "absent":
        if replace_existing:
            result.msg = f"cannot mix 'delete_unused' with 'state: {state}'"
            result.rc = 1
        else:
            result = pkg_delete(
                module,
                delete_unused=delete_unused,
                force=force,
                name=name,
                state=state,
            )
    elif state in ["latest", "present"]:
        if delete_unused:
            result.msg = f"cannot mix 'delete_unused' with 'state: {state}'"
            result.rc = 1
        else:
            result = pkg_add(
                module,
                force=force,
                name=name,
                replace_existing=replace_existing,
                state=state,
            )

    # Handle results
    if result.rc != 0:
        module.fail_json(**result.__dict__)
    module.exit_json(**result.__dict__)


if __name__ == "__main__":
    main()
