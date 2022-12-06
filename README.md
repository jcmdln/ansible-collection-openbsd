This repository provides an Ansible collection for performing actions against
OpenBSD hosts.

If you are looking for a hosting provider that offers OpenBSD, consider using
[OpenBSD.Amsterdam](https://openbsd.amsterdam) which contributes to
[The OpenBSD Foundation](https://www.openbsdfoundation.org/).

# Using

## Install

### pip

```sh
python3 -m venv .venv/bin/activate
. .venv/bin/activate
pip install .
ansible-galaxy collection install .
```

### poetry

```sh
poetry install --only root
poetry run ansible-galaxy collection install .
```

## Prepare

### Inventory

```sh
# Create an Ansible inventory
cp inventory/vagrant.yml inventory.yml
vi inventory.yml
```

## Run

### Modules

Ansible allows running modules in an adhoc fashion for one-off tasks:

```sh
ansible -i <inventory> all -m jcmdln.openbsd.pkg -a "name=htop state=present"
```

For more info, see the following:

- https://docs.ansible.com/ansible/latest/command_guide/intro_adhoc.html

### Playbooks

In this example we chain playbooks to patch/upgrade hosts and update packages:

```sh
ansible-playbook -i inventory.yml \
    site-check.yml site-syspatch.yml site-sysupgrade.yml site-pkg.yml
```

For more info, see the following:

- https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html
