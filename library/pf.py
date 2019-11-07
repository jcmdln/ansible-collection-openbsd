#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Johnathan C. Maudlin <jcmdln@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import)
from ansible.module_utils.basic import AnsibleModule


# https://man.openbsd.org/pfctl.8
def pfctl(module, result):
    return result


# https://man.openbsd.org/pfsync.4
def pfsync(module, result):
    return result


def main():
    module = AnsibleModule(
        argument_spec={
        },
        supports_check_mode=True
    )

    result = {
        'changed': False,
        'command': '/usr/sbin/syspatch',
        'msg': 'no action performed',
        'rc': 0,
        'stdout': '',
        'stderr': '',
    }

    if result['rc'] > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == '__main__':
    main()
