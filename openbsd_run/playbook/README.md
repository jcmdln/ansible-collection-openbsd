The Ansible playbooks are the main thing I'm working through at the moment, so
that they are of decent quality and can be customized painlessly.  This list is
mostly for show, as very little has actually been made usable or reasonable.

    # Meta
    site-check.yaml      - Check host(s) meet playbook requirements

    # Management / Operations
    site-pkg.yaml        - Manage package(s)
    site-syspatch.yaml   - Patch host(s) using syspatch
    site-sysupgrade.yaml - Upgrade host(s) using sysupgrade

    # Services
    site-bpg.yaml        - Setup a BGP server
    site-dns.yaml        - Setup a DNS server
    site-mail.yaml       - Setup a mail server
    site-mirror.yaml     - Setup an OpenBSD mirror
    site-ntp.yaml        - Setup a NTP server
    site-vpn.yaml        - Setup a IKEv2 or Wireguard VPN client/server

Something I want to play around with is the idea of bundling individual services
in a way that somewhat implements modern equivalents.  Rather than being treated
as standalone utilities, they would be configured to mostly handle what the
modern cloud-native options do:

    # Service Mesh (Consul, Istio)
    site-relayd.yaml     - Setup a load balancer
    site-router.yaml     - Setup a router
    site-switch.yaml     - Setup a switch
    site-unbound.yaml    - Setup a validating DNS resolver

I don't know how far I'll take this idea, but it'll be long after all the core
pieces are in an adequate state.
