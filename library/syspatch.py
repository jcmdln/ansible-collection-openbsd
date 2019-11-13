#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Johnathan C. Maudlin <jcmdln@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import)
from ansible.module_utils.basic import AnsibleModule


def syspatch_apply(r, module):
    r['rc'], r['stdout'], r['stderr'] = module.run_command(
        r['command'], check_rc=False
    )

    if r['rc'] != 0:
        r['msg'] = 'received a non-zero exit code'
        r['rc'] = 1
    elif len(r['stdout']) < 1:
        r['msg'] = 'nothing to do'
    else:
        r['msg'] = 'patches applied, probably'
        r['changed'] = True

    return r


def syspatch_list(r, module, List):
    if List == 'available':
        r['command'] = "%s -c" % (r['command'])

    if List == 'installed':
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


def syspatch_revert(r, module, Revert):
    if Revert == 'all':
        r['command'] = "%s -R" % (r['command'])

    if Revert == 'latest':
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

    return r


def main():
    module_args = {
        'apply': {
            'type': 'bool',
            'default': False,
        },
        'list': {
            'type': 'str',
            'choices': ['available', 'installed']
        },
        'revert': {
            'type': 'str',
            'choices': ['all', 'latest']
        },
    }

    module = AnsibleModule(
        argument_spec=module_args,
        required_one_of=[['apply', 'list', 'revert']],
        mutually_exclusive=[['apply', 'list', 'revert']],
        supports_check_mode=False
    )

    result = {
        'changed': False,
        'command': '/usr/sbin/syspatch',
        'msg': 'no action performed',
        'rc': 0,
        'stdout': '',
        'stderr': '',
    }

    Apply = module.params['apply']
    List = module.params['list']
    Revert = module.params['revert']

    if Apply in ['yes', True]:
        result = syspatch_apply(result, module)

    if List in ['available', 'installed']:
        result = syspatch_list(result, module, List)

    if Revert in ['yes', True]:
        result = syspatch_revert(result, module, Revert)

    if result['rc'] > 0:
        module.fail_json(**result)
    else:
        module.exit_json(**result)


if __name__ == '__main__':
    main()
