OpenBSD appliances using Ansible.


# About
This project was initially created to solve a one-dimensional problem,
though has been expanded to ask/answer the following:

1. After installing Python, OpenBSD and Ansible work quite well
together. How can we make it better?

2. Many OpenBSD utilities and services such as
[vmm(4)](https://man.openbsd.org/vmm.4) would benefit from more users
running the software and reporting bugs.  How can we make it easier to
deploy OpenBSD in a variety of scenarios?


# Usage
Run this playbook:

    $ ansible-playbook deploy.yml


Update hosts using
[sysupgrade(8)](https://man.openbsd.org/sysupgrade.8) and
[syspatch(8)](https://man.openbsd.org/syspatch.8):

    $ ansible-playbook update.yml


# Roles
openbsd.ansible
openbsd.bgpd
openbsd.grafana
openbsd.httpd
openbsd.iked
openbsd.ldapd
openbsd.mail
openbsd.mirror
openbsd.nameserver
openbsd.pf
openbsd.prometheus
openbsd.relayd
openbsd.router
openbsd.switch
openbsd.update
openbsd.vmm
openbsd.www
