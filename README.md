This repository provides an Ansible collection for performing actions against
OpenBSD hosts.

If you are looking for a hosting provider that offers OpenBSD, consider using
[OpenBSD.Amsterdam](https://openbsd.amsterdam) which contributes to
[The OpenBSD Foundation](https://www.openbsdfoundation.org/).

# Using

```sh
# Install the collection
ansible-galaxy collection install git+https://github.com/jcmdln/ansible-collection-openbsd

# Adhoc use of a module
ansible -i <inventory> all -m jcmdln.openbsd.pkg -a "name=htop state=present"

# Use a provided playbook to ensure Python is installed
ansible-playbook -i <inventory> jcmdln.openbsd.python

# Chain playbooks to patch hosts and update packages
ansible-playbook -i <inventory> jcmdln.openbsd.{syspatch,pkg}
```

# Developing

To avoid reinstalling the collection during each change, create a symbolic link
to your user's collections path instead of installing the collection:

```sh
mkdir -pv $HOME/.ansible/collections/ansible_collections/jcmdln &&
rm -frv $HOME/.ansible/collections/ansible_collections/jcmdln/openbsd &&
ln -fs $PWD $HOME/.ansible/collections/ansible_collections/jcmdln/openbsd
```
