# SPDX-License-Identifier: ISC
#
# Copyright (c) 2024 Johnathan C. Maudlin <jcmdln@gmail.com>

from __future__ import absolute_import, annotations, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
---
module: sysupgrade
short_description: Update to the next release or snapshot with sysupgrade
version_added: "1.2.0"

author: Johnathan Craig Maudlin (@jcmdln) <jcmdln@gmail.com>
description: []

options:
  branch:
    description:
    default:
  force:
    description:
    default:
  keep:
    description:
    default:
"""


class Result:
    changed: bool = False
    command: str = "/usr/sbin/sysupgrade -n"
    msg: str = ""
    rc: int = 0
    reboot: bool = False
    stdout: str = ""
    stderr: str = ""


def sysupgrade(module: AnsibleModule) -> Result:
    r: Result = Result()

    if module.params["branch"] == "release":
        r.command = f"{r.command} -r"
    elif module.params["branch"] == "snapshot":
        r.command = f"{r.command} -s"

    if module.params["force"]:
        r.command = f"{r.command} -f"

    r.rc, r.stdout, r.stderr = module.run_command(r.command, check_rc=False)

    if not r.stdout and not r.stderr:
        r.msg = "no actions performed"
        return r
    if "already on latest" in r.stdout.lower():
        r.msg = r.stdout.split("\n")[-1].strip(".").lower()
        return r
    if "404 not found" in r.stderr.lower():
        r.msg = "no newer {} available".format(module.params["branch"])
        r.rc = 0
        return r
    if r.rc != 0 or "failed" in [
        r.stderr.lower(),
        r.stdout.lower(),
    ]:
        r.msg = "failed to upgrade host"
        r.rc = 1 if r.rc == 0 else r.rc
        return r

    r.changed = True
    r.msg = "upgrade performed successfully"
    r.reboot = True
    return r


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

    result: Result = sysupgrade(module)
    if result.rc > 0:
        module.fail_json(**result.__dict__)
    module.exit_json(**result.__dict__)


if __name__ == "__main__":
    main()
