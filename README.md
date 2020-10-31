**An OpenBSD-focused Ansible playbook embedded in type-annotated Python**

This is a work-in-progress that at times may require you are well-versed in
Ansible, Python, and OpenBSD.  Things are likely to not work at all or be
extremely awkward, and until I get Ansible Molecule working with vmm(4) the
prospect of verifying anything involves manual action.


Usage
====================

Playbook
--------------------
The [raw playbook](./openbsd_run/playbook/README.md) can be used without any
atypical Ansible setup or intrinsic dependencies to the command line interface
for those who might prefer it.


Command Line Interface
--------------------
The command line interface is a type-annotated Python wrapper for the included
Ansible playbook, which allows for simpler packaging and distribution in a way
that should feel familiar to Python users or package maintainers

### Installing
You may use poetry, pip, or some equivalent Python package manager. Some
examples are provided below, though this is not intended to be exhaustive.

#### poetry
```sh
    $ poetry install git+https://github.com/jcmdln/openbsd-run.git
```

#### pip
```sh
    $ pip install git+https://github.com/jcmdln/openbsd-run.git
```

### Running
The command line interface may be used by installing this repository as a Python
package using pip, poetry, or other such tools.

```sh
    $ openbsd-run -h
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

### Subcommand Example

```sh
    $ openbsd-run -i sample.inventory.yml pkg-add -h
    Usage: openbsd-run pkg-add [OPTIONS] PACKAGES

    Options:
      -D TEXT     Force package install, waiving the specified failsafe
      -u          Update named packages, installing any missing packages
      -h, --help  Show this message and exit.
```
