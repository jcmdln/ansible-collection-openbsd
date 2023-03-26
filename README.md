This repository provides an Ansible collection for performing actions against
OpenBSD hosts.

If you are looking for a hosting provider that offers OpenBSD, consider using
[OpenBSD.Amsterdam](https://openbsd.amsterdam) which contributes to
[The OpenBSD Foundation](https://www.openbsdfoundation.org/).

# Using

## As a Playbook

```sh
# Install Ansible
sudo dnf -y install ansible-core

# Create an inventory
cp inventory/vagrant.yml inventory.yml
vi inventory.yml

# Run a playbook
ansible-playbook -i inventory.yml site-check.yml
```

In this example we chain playbooks to patch/upgrade hosts and update packages:

```sh
ansible-playbook -i inventory.yml \
    site-check.yml site-syspatch.yml site-sysupgrade.yml site-pkg.yml
```

For more info, see the following:

- https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html

## As a Collection

```sh
ansible-galaxy collection install git+https://github.com/jcmdln/ansible-collection-openbsd
```

Ansible allows running modules in an adhoc fashion for one-off tasks:

```sh
ansible -i <inventory> all -m jcmdln.openbsd.pkg -a "name=htop state=present"
```

For more info, see the following:

- https://docs.ansible.com/ansible/latest/command_guide/intro_adhoc.html
