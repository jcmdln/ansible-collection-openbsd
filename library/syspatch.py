#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Johnathan C. Maudlin <jcmdln@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import)
from ansible.module_utils.basic import AnsibleModule


def syspatch_apply(r, module, choice):
    r['rc'], r['stdout'], r['stderr'] = module.run_command(
        r['command'],
        check_rc=False
    )

    if r['rc'] != 0:
        r['msg'] = 'received a non-zero exit code'
        r['rc'] = 1
    elif len(r['stdout']) < 1:
        r['msg'] = 'nothing to do'
    else:
        r['msg'] = 'patches applied, probably'
        r['changed'] = True

        if 'reboot to load the new kernel' in r['stdout']:
            r['restart'] = True

    return r


def syspatch_list(r, module, choice):
    if choice == 'available':
        r['command'] = "%s -c" % (r['command'])
    if choice == 'installed':
        r['command'] = "%s -l" % (r['command'])

    r['rc'], r['stdout'], r['stderr'] = module.run_command(
        r['command'],
        check_rc=False
    )

    if r['rc'] != 0:
        r['msg'] = 'received a non-zero exit code'
        r['rc'] = 1
    elif len(r['stdout']) < 1:
        r['msg'] = 'nothing to do'
    else:
        r['msg'] = 'list of patches returned'

    return r


def syspatch_revert(r, module, choice):
    if choice == 'all':
        r['command'] = "%s -R" % (r['command'])
    if choice == 'latest':
        r['command'] = "%s -r" % (r['command'])

    r['rc'], r['stdout'], r['stderr'] = module.run_command(
        r['command'],
        check_rc=False
    )

    if r['rc'] != 0:
        r['msg'] = 'received a non-zero exit code'
        r['rc'] = 1
    elif len(r['stdout']) < 1:
        r['msg'] = 'nothing to do'
    else:
        r['msg'] = 'patches reverted, probably'
        r['changed'] = True

        if 'reboot to load the new kernel' in r['stdout']:
            r['restart'] = True

    return r


def main():
    module = AnsibleModule(
        argument_spec={
            'apply': {
                'type': 'bool',
                'default': False,
                'required': False
            },

            'list': {
                'type': 'str',
                'choices': [
                    'available',
                    'installed'
                ],
                'required': False
            },

            'revert': {
                'type': 'bool',
                'default': False,
                'required': False
            },

            'state': {
                'type': 'str',
                'choices': [
                    'absent',
                    'latest',
                    'present'
                ],
            },
        },

        required_one_of=[
            ['apply', 'list', 'revert']
        ],

        mutually_exclusive=[
            ['apply', 'list', 'revert'],
            ['list', 'state'],
        ],

        supports_check_mode=False
    )

    result = {
        'changed': False,
        'command': '/usr/sbin/syspatch',
        'msg': 'no action performed',
        'restart': False,
        'rc': 0,
        'stdout': '',
        'stderr': '',
    }

    Apply = module.params['apply']
    List = module.params['list']
    Revert = module.params['revert']
    State = module.params['state']

    if Apply in ['yes', True]:
        Apply = True
        result = syspatch_apply(result, module, Apply, State)

    if List in ['available', 'installed']:
        result = syspatch_list(result, module, List)

    if Revert in ['yes', True]:
        Revert = True
        result = syspatch_revert(result, module, Revert, State)

    if result['rc'] > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == '__main__':
    main()
