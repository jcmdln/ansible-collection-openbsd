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
