**An OpenBSD-focused Ansible playbook embedded in type-annotated Python**

`openbsd-run` is an Ansible playbook embedded in type-annotated Python which
allows for running the Ansible playbooks directly or via command line.

NOTE: This is a work-in-progress that at times may require you are well-versed
in Ansible, Python, and OpenBSD.  Things are likely to not work at all or be
extremely awkward, and until I get Ansible Molecule working with vmm(4) the
prospect of verifying anything involves manual action.


Usage
====================
The [raw playbook](./openbsd_run/playbook/) can be used without any atypical
Ansible setup or intrinsic dependencies to the command line interface for those
who might prefer it. See the [README.md](./openbsd_run/playbook/README.md) for
more information.


Command Line Interface
--------------------
The command line interface provides familiar commands for performing actions
against hosts defined in an [inventory](./sample.inventory.yml) that directly
use the [raw playbook](./openbsd_run/playbook/) files. The main benefit of this
is that you may define a simple inventory that can be dynamically acted upon
but there's no _real_ functional difference between the two flows other than
the CLI exposes only what _appears_ to be ready for broader use.

### Installing
You may use poetry, pip, or some equivalent Python package manager. Some
examples are provided below, though this is not intended to be exhaustive.

#### pip
Pip should work exactly as you would expect, and the following example does not
need to be followed literally.

```sh
$ git clone --branch master https://github.com/jcmdln/openbsd-run
$ cd openbsd-run
$ virtualenv .venv
$ source .venv/bin/activate
(.venv) $ pip install git+https://github.com/jcmdln/openbsd-run@master
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

#### poetry
When using [Poetry](https://github.com/python-poetry/poetry) the virtualenv
will automatically be created as `.venv`, and doesn't have to be activated
unless you prefer to do so.

```sh
$ git clone --branch master https://github.com/jcmdln/openbsd-run
$ cd openbsd-run
$ poetry install --no-dev
$ poetry run openbsd-run
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
Looking at the help output of subcommands is a little weird for now, as it
requires that you have provided an inventory file. In the future I'll allow
using a configuration file at `/etc/openbsd-run/inventory.{cfg,yaml}` or loosen
the check for a valid file if `-h|--help` was passed. Likely both.

```sh
$ openbsd-run -i sample.inventory.yml pkg-add -h
Usage: openbsd-run pkg-add [OPTIONS] PACKAGES

Options:
  -D TEXT     Force package install, waiving the specified failsafe
  -u          Update named packages, installing any missing packages
  -h, --help  Show this message and exit.
```


Contributing
==========
The primary goal of this project is to make doing native OpenBSD "things" from
a remote system trivially possible. General administration and setting up a
mirror are two good examples, and you're likely to see scaffolding in the
[raw playbook](./openbsd_run/playbook/).

* If anything seems weird, definitely report it
* For starting new work, please file an issue so it may be discussed
