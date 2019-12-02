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
