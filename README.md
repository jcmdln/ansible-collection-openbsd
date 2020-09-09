openbsd.run
====================

This project marries a complete Ansible playbook within type-annotated Python
specifically to simplify configuration of OpenBSD hosts.  Originally this
project was focused around making an off-shoot of OpenBSD.Amsterdam easy for
anyone to setup, though now focuses on simplifying operations tasks and setting
up services.  Everything has yet to be adapted to follow this change in goals.

Consider this project a curiosity and move on unless you are well-versed in
Ansible, Python, and OpenBSD.  Things are likely to not work at all or be
extremely awkward, and until I get Ansible Molecule working with vmm(4) the
prospect of verifying anything involves manual action.


Playbooks
--------------------
The raw playbook can be used without any atypical Ansible setup or intrisic
dependencies to the command line interface, and is located
[here](./openbsd_run/playbook).

The Ansible playbooks are the main thing I'm working through at the moment, so
that they are of decent quality and can be customized painlessly.  This list is
mostly for show, as very little has actually been made usable or reasonable.

    # Meta
	site-check.yml      - Check host(s) meet playbook requirements

	# Management / Operations
	site-pkg.yml        - Manage package(s)
	site-syspatch.yml   - Patch host(s) using syspatch
	site-sysupgrade.yml - Upgrade host(s) using sysupgrade

	# Services
	site-bpg.yml        - Setup a BGP server
	site-dns.yml        - Setup a DNS server
	site-firewall.yml   - Setup a firewall
	site-mail.yml       - Setup a mail server
	site-mirror.yml     - Setup an OpenBSD mirror
	site-ntp.yml        - Setup an NTP server
	site-pxe.yml        - Setup a PXE server
	site-relayd.yml     - Setup a load balancer
	site-router.yml     - Setup a router
	site-switch.yml     - Setup a switch
	site-unbound.yml    - Setup a validating DNS resolver
	site-unwind.yml     - Setup a local DNS resolver
	site-vmd.yml        - Setup host(s) to run virtual machines
	site-vpn.yml        - Setup a IKEv2 or Wireguard VPN client/server

### Extras
Something I want to play around with is the idea of bundling individual services
in a way that somewhat implements modern equivalents.  Rather than being treated
as standalone utilities, they would be configured to mostly handle what the
modern cloud-native options do:

    # Service Mesh (Consul, Istio)
	site-relayd.yml     - Setup a load balancer
	site-router.yml     - Setup a router
	site-switch.yml     - Setup a switch
	site-unbound.yml    - Setup a validating DNS resolver

I don't know how far I'll take this idea, but it'll be long after all the core
pieces are in an adequate state.


Commands
--------------------
The command line interface may be used by installing this repository as a Python
package using pip, poetry, or other such tools.

I'm trying to work out some sort of reasonable behavior for the command line
interface, but there are some pain points.  The commands must use the created
modules that are used within the playbook in order to be reliable, otherwise you
would be using something like fabric to run arbitrary commands.  Because of
this, the commands as provided by the cli will be limited to interactions that
are able to be provided in both workflows, prioritizing Ansible playbooks since
that's the primary purpose of this project.

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
	  pkg-add     Add or update packages
	  syspatch    Patch host(s) using syspatch
	  sysupgrade  Upgrade host(s) using sysupgrade

An issue is that the global options as listed above are propagated to
subcommands, though subcommands themselves do not declare that they receive
these options.  This leads to a weird command line interface and output as shown
below:

	$ openbsd-run -i sample.inventory.yml pkg-add -h
	Usage: openbsd-run pkg-add [OPTIONS] PACKAGES

	Options:
	  -D TEXT     Force package install, waiving the specified failsafe
	  -u          Update named packages, installing any missing packages
	  -h, --help  Show this message and exit.
