# openbsd.run

This project marries a complete Ansible playbook within type-annotated Python
specifically to simplify configuration of OpenBSD hosts.  Originally this
project was focused around making an off-shoot of OpenBSD.Amsterdam easy for
anyone to setup, though now focuses on simplifying operations tasks and setting
up services.  Everything has yet to be adapted to follow this change in goals.

Consider this project a curiosity and move on unless you are well-versed in
Ansible, Python, and OpenBSD.  Things are likely to not work at all or be
extremely awkward, and until I get Ansible Molecule working with vmm(4) the
prospect of verifying anything involves manual action.


## Playbooks
The Ansible playbooks are the main thing I'm working through at the moment, so
that they are of decent quality and can be customized painlessly.

```
# Individual plays
site-check.yml      - Check host(s) meet requirements
site-dns.yml        - Prepare host(s) as a DNS server
site-firewall.yml   - Prepare host(s) as a firewall
site-mail.yml       - Prepare host(s) as a mail server
site-packages.yml   - Manage packages
site-syspatch.yml   - Run syspatch
site-sysupgrade.yml - Run sysupgrade
site-vmd.yml        - Prepare host(s) to run VMM
```

## Commands
Eventually I would like to have a nearly 1:1 mapping of running ad-hoc commands
that perform the expected task.  Since these will require the use of the modules
specific to this repository, some slight alterations or limitations in scope
will be unavoidable.

When this is implemented, I will fully support Ansible's syntax for performing
these actions on arbitrary hosts, which should mostly work out of the box aside
from contextual errors:

```
openbsd-run -i inventory.yml host[1-3].domain.tld <command>
```
