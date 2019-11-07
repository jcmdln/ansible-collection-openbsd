#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Johnathan C. Maudlin <jcmdln@gmail.com>
#
# GNU General Public License v3.0+ (see COPYING or
# https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import)
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: sysupgrade
short_description: Upgrade OpenBSD to the next release or snapshot
version_added: "2.9"

description:
    - Use the sysupgrade(8) utility to upgrade a system to the next
      release or the latest snapshot for OpenBSD 6.6 or later.

options:
    upgrade:
        description:
            - Upgrade to the next release or latest snapshot.
        type: bool
        default: false
        required: true
    force:
        description:
            - Force an already applied upgrade.  This option has no
              effect on releases.
        type: bool
        default: false
        required: false
    keep:
        description:
            - Keep the files in /home/_sysupgrade
        type: bool
        default: false
        required: false

author:
    - Johnathan C Maudlin (@jcmdln)
'''

EXAMPLES = '''
- name: Upgrade to latest release or snapshot
  when:
    - ansible_distribution == 'OpenBSD'
    - ansible_distribution_version >= '6.5' and ansible_distribution_release == 'current' or
      ansible_distribution_version >= '6.6'
  register: result
  sysupgrade:
    upgrade: yes

- name: Reboot if upgrade performed
  when:
    - 'result is succeeded'
    - result.changed == true
  reboot:
'''

RETURN = '''
changed:
    description: A change on the host was reported
    returned: always
    type: bool
command:
    description: The command and arguments that were used
    returned: always
    type: str
msg:
    description: The message returned by the command
    returned: always
    type: str
rc:
    description: The command return code (0 means success)
    returned: always
    type: int
stderr:
    description: sysupgrade standard error
    returned: always
    type: str
stdout:
    description: sysupgrade standard output
    returned: always
    type: str
'''


def upgrade(r, module, force, keep):
    if force:
        r['command'] = "%s -f" % (r['command'])
    if keep:
        r['command'] = "%s -k" % (r['command'])

    r['rc'], r['stdout'], r['stderr'] = module.run_command(
        r['command'], check_rc=False
    )

    if 'ftp: Error retrieving file: 404 Not Found' in r['stderr']:
        # This signifies that no later release is available, so catch
        # this error and propagate the details.
        r['rc'] = 0
        r['msg'] = 'already on the latest available release'
    elif r['rc'] != 0:
        r['changed'] = False
        r['msg'] = 'received a non-zero exit code'
    elif 'Already on latest' in r['stdout']:
        r['changed'] = False
        r['msg'] = 'no action required'
    else:
        if 'Will upgrade on next reboot' in r['stdout']:
            r['changed'] = True
            r['msg'] = 'Upgrade prepared successfully'
        else:
            r['changed'] = True
            r['msg'] = "something isn't right"

    return r


def main():
    module = AnsibleModule(
        argument_spec={
            'upgrade': {
                'type': 'bool',
                'required': True,
            },
            'force': {
                'type': 'bool',
                'default': False,
            },
            'keep': {
                'type': 'bool',
                'default': False,
            },
        },

        supports_check_mode=True
    )

    r = {
        'changed': False,
        'command': '/usr/sbin/sysupgrade -n',
        'msg': 'no action performed',
        'restart': False,
        'rc': 0,
        'stderr': '',
        'stdout': '',
    }

    p = module.params

    if p['upgrade'] in ['yes', True]:
        p['upgrade'] = True

        if p['force'] in ['yes', True]:
            p['force'] = True

        if p['keep'] in ['yes', True]:
            p['keep'] = True

        r = upgrade(r, module, p['force'], p['keep'])

    if r['rc'] == 1:
        module.fail_json(**r)
    else:
        module.exit_json(**r)


if __name__ == '__main__':
    main()
