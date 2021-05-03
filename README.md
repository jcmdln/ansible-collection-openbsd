**An OpenBSD-focused Ansible playbook embedded in type-annotated Python**

[openbsd-run](https://github.com/jcmdln/openbsd-run) is an Ansible playbook
embedded in type-annotated Python which allows for running the Ansible
playbooks directly or via command line. The goal is to trivialize deploying and
maintaining OpenBSD-based services.

NOTE: This is a work-in-progress that at times may require you are well-versed
in Ansible, Python, and OpenBSD.  Things are likely to not work at all or be
extremely awkward, and until I get Ansible Molecule working with vmm(4) the
prospect of verifying anything involves manual action.


# Usage
This project only supports OpenBSD. You may test it by using the included
Vagrantfile or by setting up an instance on a hosting provider. If you are
looking for a hosting provider that provides OpenBSD, consider using
[OpenBSD.Amsterdam](https://openbsd.amsterdam) which donates some proceeds to
[The OpenBSD Foundation](https://www.openbsdfoundation.org/).

## Playbook
The [raw playbook](./openbsd_run/playbook/) can be used without any atypical
Ansible setup or intrinsic dependencies to the command line interface for those
who might prefer it.

## Command Line Interface
The command line interface provides familiar commands for performing actions
against hosts defined in an [inventory](./sample.inventory.yml). The main
benefit of this is that you may define a simple inventory that can be
dynamically acted upon without also needing to define or consume playbooks.

### Installing
As shown in the following example, we suggest using `--system-site-packages` as
this will greatly reduce the total installation size if you already have
Ansible and build time if you already have py3-cryptography.

```sh
    $ virtualenv --system-site-packages .venv
    $ source .venv/bin/activate
    (.venv) $ pip install .
    (.venv) $ openbsd-run -h
    Usage: openbsd-run [OPTIONS] COMMAND [ARGS]...

    Options:
      -H, --host_pattern TEXT  Host pattern to match against inventory
      -i, --inventory TEXT     Inventory file
      -q, --quiet              Suppress Ansible output
      -V, --verbose            Increase Ansible output
      -v, --version            Show the version and exit.
      -h, --help               Show this message and exit.

    Commands:
      pkg_add     Add or update packages
      pkg_delete  Remove packages
      syspatch    Patch host(s) using syspatch
      sysupgrade  Upgrade host(s) using sysupgrade
```


# Contributing
The primary goal of this project is to make doing native OpenBSD "things" from
a remote system trivially possible. General administration and setting up a
mirror are two good examples, and you're likely to see scaffolding in the
[raw playbook](./openbsd_run/playbook/).

* If anything seems weird, definitely report it
* For starting new work, please file an issue so it may be discussed
