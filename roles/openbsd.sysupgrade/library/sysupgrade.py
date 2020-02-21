#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Johnathan C. Maudlin <jcmdln@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import)
from ansible.module_utils.basic import AnsibleModule


def upgrade(r, module, Branch, Force):
    if Branch == 'release':
        r['command'] = "%s -r" % (r['command'])
    elif Branch == 'snapshot':
        r['command'] = "%s -s" % (r['command'])

    if Force:
        r['command'] = "%s -f" % (r['command'])

    r['rc'], r['stdout'], r['stderr'] = module.run_command(
        r['command'], check_rc=False
    )

    if 'ftp: Error retrieving file: 404 Not Found' in r['stderr']:
        # This signifies that no later release is available, which
        # isn't really an error.
        r['rc'] = 0
        r['msg'] = 'already on the latest available release'
    elif r['rc'] > 0:
        r['changed'] = False
        r['msg'] = 'received a non-zero exit code'
    elif 'Already on latest' in r['stdout']:
        r['changed'] = False
        r['msg'] = 'no action required'
    elif 'Will upgrade on next reboot' in r['stdout']:
        r['changed'] = True
        r['msg'] = 'Upgrade prepared successfully'
    else:
        r['changed'] = True
        r['msg'] = "something unexpected happened"
        r['rc'] = 1

    return r


def main():
    module_args = {
        'branch': {
            'type': 'str',
            'choices': ['auto', 'release', 'snapshot'],
        },
        'force': {
            'type': 'bool',
            'default': False,
        },
    }

    module = AnsibleModule(
        argument_spec=module_args,
        required_one_of=[['branch']],
        supports_check_mode=True,
    )

    result = {
        'changed': False,
        'command': '/usr/sbin/sysupgrade -n',
        'msg': 'no action performed',
        'rc': 0,
        'stderr': '',
        'stdout': '',
    }

    Branch = module.params['branch']
    Force = module.params['force']

    if Force in ['yes', True]:
        Force = True

    if Branch in ['auto', 'release', 'snapshot']:
        result = upgrade(result, module, Branch, Force)

    if result['rc'] > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == '__main__':
    main()
