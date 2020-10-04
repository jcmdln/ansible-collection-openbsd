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
