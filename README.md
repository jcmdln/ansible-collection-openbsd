Create modular, standalone appliances for OpenBSD using Ansible roles


About
=====
After installing Python, OpenBSD and Ansible work quite well together.

How can we make it better?

* Look for areas of improvement in OpenBSD and Ansible
* Catalog existing Ansible modules and create what's missing
* Refer to official sources (man.openbsd.org, openbsd.org/faq)
* Verify all roles with signify(8)
* Support git & got in all repositories


Modules
=======
Ansible provides "out-of-the-box" support by having an extensive set of
[modules](https://docs.ansible.com/ansible/latest/modules/list_of_all_modules.html)
for basically everything.  In terms of what's provided in OpenBSD, is
anything missing?

### got(8)
Didn't look for an existing module, though it would be nice to have.

### pkg_*
Using Ansible to install packages is a common tactic, though what sort
of support for this exists?

Currently there is an
[openbsd_pkg](https://docs.ansible.com/ansible/latest/modules/openbsd_pkg_module.html)
module which provides most of what you'd expect from the `pkg_*`
utilities.  It's missing an equivalent of `pkg_add -D`, which when
using sysupgrade(8) to upgrade to a newer snapshot is pretty important.

### signify(8)
Didn't look for an existing module, but I'd like to be able to download
stuff and _verify_ it.

### sysmerge
sysupgrade(8) makes writing this module not so useful, though I want to
track it for now.

### syspatch(8)
A module did exist at one point, though I've written my own.

### sysupgrade(8)
Didn't look too hard, decided to write my own.

### vmm(4)
jasperla@ wrote
[vmm modules](https://github.com/jasperla/ansible-vmm/tree/master/library)
that are quite stale, and could use a cleanup pass.


Roles
=====
Each role should be a standalone appliance, meaning that each role should
be for a single goal.  A role may require interacting with a number of
utilities, but _must_ not require the use of other roles.


Misc
----
Stuff that probably ends up in multiple roles

* https://man.openbsd.org/cron.8
* https://man.openbsd.org/crontab.1
* https://man.openbsd.org/crontab.5
* https://man.openbsd.org/httpd.8
* https://man.openbsd.org/httpd.conf.5
* https://man.openbsd.org/relayd.8
* https://man.openbsd.org/relayd.conf.5
* https://man.openbsd.org/ssl.8


openbsd_ansible.auth
--------------------
Configure a host as an authentication server/client

### Sources
* TBD

### Utilities
* https://man.openbsd.org/acme-client.1
* https://man.openbsd.org/acme-client.conf.5
* https://man.openbsd.org/ldapd.8


openbsd_ansible.dns
--------------------
Configure a host as a DNS server

### Sources
* TBD

### Manuals
* https://man.openbsd.org/nsd.8
* https://man.openbsd.org/nsd.conf.5
* https://man.openbsd.org/nsd-checkconf.8
* https://man.openbsd.org/unbound.8
* https://man.openbsd.org/unbound.conf.5
* https://man.openbsd.org/unbound-checkconf.8


openbsd_ansible.firewall
--------------------
Configure a host as a firewall

### Sources
* TBD

### Manuals
* https://man.openbsd.org/pf.4
* https://man.openbsd.org/pfctl.8


openbsd_ansible.mail
--------------------
Configure a host as a mail server

### Sources
* TBD

### Manuals
* https://man.openbsd.org/smtp.1
* https://man.openbsd.org/smtpd.8
* https://man.openbsd.org/smtpd.conf.5
* https://man.openbsd.org/spamd.8
* https://man.openbsd.org/spamd.conf.5


openbsd_ansible.router
--------------------
Configure a host as a router

### Sources
* https://www.openbsd.org/faq/pf/example1.html

### Manuals
* https://man.openbsd.org/bgpd.8
* https://man.openbsd.org/dhcpd.8
* https://man.openbsd.org/pf.4
* https://man.openbsd.org/pfctl.8


openbsd_ansible.storage
--------------------
Configure a host as a storage appliance

### Sources
* https://www.openbsd.org/faq/faq6.html#NFS

### Manuals
* https://man.openbsd.org/ftp.1
* https://man.openbsd.org/ftpd.8
* https://man.openbsd.org/nfsd.8
* https://man.openbsd.org/softraid.4


openbsd_ansible.update
--------------------
This role updates OpenBSD hosts

### Sources
* TBD

### Manuals
* https://man.openbsd.org/syspatch.8
* https://man.openbsd.org/sysupgrade.8


openbsd_ansible.vmm
--------------------
Configure a host as a virtualization appliance

### Sources
* https://www.openbsd.org/faq/faq16.html

### Manuals
* https://man.openbsd.org/vmctl.8
* https://man.openbsd.org/vmd.8
* https://man.openbsd.org/vmm.4


openbsd_ansible.vpn
--------------------
Configure a host to provide or use a VPN

### Sources
* https://www.openbsd.org/faq/faq17.html

### Manuals
* https://man.openbsd.org/ikectl.8
* https://man.openbsd.org/iked.8


Testing
=======

`molecule` is a framework allows for testing roles and playbooks though
primarily targets Docker and Vagrant.  Is it possible to use Vagrant as
an example, and provide support for `vmm(8)`?
