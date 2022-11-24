This repository provides an Ansible collection for performing actions against
OpenBSD hosts.

If you are looking for a hosting provider that offers OpenBSD, consider using
[OpenBSD.Amsterdam](https://openbsd.amsterdam) which contributes to
[The OpenBSD Foundation](https://www.openbsdfoundation.org/).

# Setup

## Dependencies

```sh
# Create a virtualenv and activate it
virtualenv .venv
source .venv/bin/activate
# Install Python dependencies
pip install -r requirements.txt
# Install Ansible dependencies
ansible-galaxy collection install .
```

## Inventory

```sh
# Create an Ansible inventory
cp inventory/vagrant.yml inventory.yml
vi inventory.yml
```

## Run playbook(s)

For documentation and examples of how to use each playbook, please see
[docs/playbooks.md](docs/playbooks.md) for more information.

```sh
# Example of chaining playbooks to patch/upgrade hosts and update packages
ansible-playbook -i inventory.yml \
    site-check.yml site-syspatch.yml site-sysupgrade.yml site-pkg.yml
```

## Vagrant

### Fedora

```sh
sudo dnf install libvirt-devel rubygems-rexml vagrant --excludepkgs vagrant-libvirt
vagrant plugin install
```
