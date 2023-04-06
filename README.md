This repository provides an Ansible collection for performing actions against
OpenBSD hosts.

If you are looking for a hosting provider that offers OpenBSD, consider using
[OpenBSD.Amsterdam](https://openbsd.amsterdam) which contributes to
[The OpenBSD Foundation](https://www.openbsdfoundation.org/).

# Using

## Collection

```sh
ansible-galaxy collection install git+https://github.com/jcmdln/ansible-collection-openbsd
```

Ansible allows running modules in an adhoc fashion for one-off tasks:

```sh
ansible -i <inventory> all -m jcmdln.openbsd.pkg -a "name=htop state=present"
```

For more info, see the following:

- https://docs.ansible.com/ansible/latest/command_guide/intro_adhoc.html

## Playbook

```sh
# Install this collection and its dependencies
ansible-galaxy collection install .

# Create a symlink to this collection so changes don't require reinstalling
rm -fr ~/.ansible/collections/ansible_collections/jcmdln/openbsd
ln -fs $PWD ~/.ansible/collections/ansible_collections/jcmdln/openbsd

# Create an inventory
cp inventory/localhost.yml inventory/example.yml
vi inventory/example.yml

# Run a playbook
ansible-playbook -i inventory/example.yml site-check.yml
```

In this example we chain playbooks to patch/upgrade hosts and update packages:

```sh
ansible-playbook -i inventory/example.yml \
    site-check.yml site-syspatch.yml site-sysupgrade.yml site-pkg.yml
```
