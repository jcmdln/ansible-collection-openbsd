This repository provides an Ansible collection which contains modules for
performing actions against OpenBSD hosts.

If you are looking for a hosting provider that offers OpenBSD, consider using
[OpenBSD.Amsterdam](https://openbsd.amsterdam) which contributes to
[The OpenBSD Foundation](https://www.openbsdfoundation.org/).

# Using

```sh
ansible-galaxy collection install git+https://github.com/jcmdln/ansible-collection-openbsd
```

Ansible allows running modules in an adhoc fashion for one-off tasks:

```sh
ansible -i <inventory> all -m jcmdln.openbsd.pkg -a "name=htop state=present"
```

For more info, see the following:

- https://docs.ansible.com/ansible/latest/command_guide/intro_adhoc.html
