[openbsd-run](https://github.com/jcmdln/openbsd-run) is an Ansible playbook
embedded in Python for performing actions against OpenBSD hosts.

If you are looking for a hosting provider that offers OpenBSD, consider using
[OpenBSD.Amsterdam](https://openbsd.amsterdam) which contributes to
[The OpenBSD Foundation](https://www.openbsdfoundation.org/).


Usage
==========
This project only supports OpenBSD. You may test it by using the included
Vagrantfile or by setting up an instance on a hosting provider.

Playbook
----------
If you would rather use the [raw playbook](./openbsd_run/playbook/) you may do
so without any atypical setup.

Command Line Interface
----------
By wrapping the Ansible playbook and the various plays with a command line
interface we can provide familiar commands that run in parallel on hosts
defined in an [inventory](./sample.inventory.yml).

### Installing
You may use `pip` instead of `poetry`, though we'll only cover using the
latter since that's what's used for running, developing and testing.
```sh
$ poetry install --no-dev
$ poetry run openbsd-run -h
Usage: openbsd-run [OPTIONS] COMMAND [ARGS]...

Options:
  -H, --host_pattern TEXT  Host pattern to match against inventory
  -i, --inventory TEXT     Ansible inventory file
  -q, --quiet              Suppress Ansible output
  -v, --verbose            Increase Ansible output
  --version                Show the version and exit.
  -h, --help               Show this message and exit.

Commands:
  pkg_add     Add or update packages
  pkg_delete  Remove packages
  syspatch    Patch host(s) using syspatch
  sysupgrade  Upgrade host(s) using sysupgrade
```


Contributing
==========
The primary goal of this project is to make doing native OpenBSD "things" from
a remote system trivially possible. General administration and setting up a
mirror are two good examples, and you're likely to see scaffolding in the
[raw playbook](./openbsd_run/playbook/).

* If anything seems weird, definitely report it
* For starting new work, please file an issue so it may be discussed

### Custom OpenBSD Vagrant box
I was originally using the `generic/openbsd7` image but Vagrant fully supports
what is needed for OpenBSD to run without adding additional packages. This
isn't required for any part of `openbsd-run` to function, test, etc but I like
having the ability to create a fresh environment to test specific things in.

I'll cover this in more detail later but here is a block of commands that I
use when building/rebuilding the image, **BUT DON'T RUN THIS VERBATIM**:
```sh
vagrant destroy -f &&
vagrant box remove openbsd-run/openbsd &&
virsh vol-list --pool default |
    awk '/openbsd-run/ {print $1}' |
    xargs virsh vol-delete --pool default --vol &&
packer build -force openbsd.pkr.hcl &&
vagrant box add openbsd-run/openbsd build/openbsd-70-amd64.box &&
vagrant up
```
