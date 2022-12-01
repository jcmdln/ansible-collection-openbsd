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

For documentation and examples of how to use each playbook, please see
[docs/playbooks.md](docs/playbooks.md) for more information.

```sh
# Example of chaining playbooks to patch/upgrade hosts and update packages
ansible-playbook -i inventory.yml \
    site-check.yml site-syspatch.yml site-sysupgrade.yml site-pkg.yml
```
