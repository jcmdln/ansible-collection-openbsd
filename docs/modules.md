Modules
=======
Ansible provides "out-of-the-box" support by having an extensive set of
[modules][Ansible modules] for basically everything.  In terms of
what's provided in OpenBSD, is anything missing?

[Ansible modules]: https://docs.ansible.com/ansible/latest/modules/list_of_all_modules.html

### pkg_add(1)
Using Ansible to install packages is a common tactic, though what sort
of support for this exists?

Currently there is an [openbsd_pkg] module which provides most of what
you'd expect from the `pkg_*` utilities.  It's missing an equivalent of
`pkg_add -D`, which when using sysupgrade(8) to upgrade to a newer
snapshot is pretty important.

[pkg_add(1)]: https://man.openbsd.org/pkg_add.1
[openbsd_pkg]: https://docs.ansible.com/ansible/latest/modules/openbsd_pkg_module.html


### signify(8)
Didn't look for an existing module, but I'd like to be able to download
stuff and _verify_ it.

[signify(8)]: https://man.openbsd.org/signify.8

### syspatch(8)
A module did exist at one point, though I've written my own.

[syspatch(8)]: https://man.openbsd.org/syspatch.8

### sysupgrade(8)
Didn't look too hard, decided to write my own.

[sysupgrade(8)]: https://man.openbsd.org/sysupgrade.8

### vmm(4)
jasperla@ wrote [vmm modules] that are quite stale, and could use a
cleanup pass.

[vmm modules]: https://github.com/jasperla/ansible-vmm/tree/master/library
