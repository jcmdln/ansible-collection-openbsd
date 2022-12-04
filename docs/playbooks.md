This file outlines how each of the top-level playbooks are used including how
they can be composed.

# site-check.yml

The `site-check.yml` playbook is intended to be run before all other playbooks
and ensures that the all hosts in an inventory are running OpenBSD and have
Python installed. Ansible requires Python, so this playbook can help to
automate running the playbooks against freshly installed OpenBSD hosts which
may not already have it installed.

```sh
ansible-playbook -i <inventory> site-check.yml
```

# site-mail.yml

The `site-mail.yml` playbook sets up a simple mail server.

```sh
ansible-playbook -i <inventory> site-pkg.yml
```

# site-pkg.yml

The `site-pkg.yml` playbook is a wrapper for the `pkg_*` suite of utilities for
managing packages on systems.

## pkg_add -u (default)

```sh
ansible-playbook -i <inventory> site-pkg.yml
```

## pkg_add

```sh
ansible-playbook -i <inventory> site-pkg.yml -e '{
    "pkg_packages": ["emacs--no_x11"],
    "pkg_state": "present",
    "pkg_title": "Install GNU/Emacs",
}'
```

## pkg_delete

```sh
ansible-playbook -i <inventory> site-pkg.yml -e '{
    "pkg_packages": ["emacs"],
    "pkg_state": "absent",
    "pkg_title": "Uninstall GNU/Emacs",
}'
```

# site-syspatch.yml

The `site-syspatch.yml` playbook

```sh
ansible-playbook -i <inventory> site-syspatch.yml
```

# site-sysupgrade.yml

The `site-sysupgrade.yml` playbook runs `sysupgrade`

## sysupgrade -r (Default)

```sh
ansible-playbook -i <inventory> site-sysupgrade.yml
```

## sysupgrade -s
