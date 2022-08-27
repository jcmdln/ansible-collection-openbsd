# site-check.yml

```sh
ansible-playbook -i inventory.yml site-check.yml
```

# site-pkg.yml

## Update packages (default)

```sh
ansible-playbook -i inventory.yml site-pkg.yml
```

## Install package(s)

```sh
ansible-playbook -i inventory.yml site-pkg.yml -e '{
    "pkg_packages": ["emacs--no_x11"],
    "pkg_state": "present",
    "pkg_title": "Install GNU/Emacs",
}'
```

## pkg_delete

```sh
ansible-playbook -i inventory.yml site-pkg.yml -e '{
    "pkg_packages": ["emacs"],
    "pkg_state": "absent",
    "pkg_title": "Uninstall GNU/Emacs",
}'
```

# site-syspatch.yml

```sh
ansible-playbook -i inventory.yml site-syspatch.yml
```

# site-sysupgrade.yml

```sh
ansible-playbook -i inventory.yml site-sysupgrade.yml
```
