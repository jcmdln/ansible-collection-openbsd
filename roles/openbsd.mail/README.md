Role Name
=========

* smtpd.8
* spamd.8

Requirements
------------

### DNS Records
* https://tools.ietf.org/html/rfc3501

| Host              | Type  | TTL  | Value |
| ----------------- | ----- | ---- | ----- |
| domain.tld        | A     | 3600 | <IPv4 Address>
| domain.tld        | AAAA  | 3600 | <IPv4 Address>
| domain.tld        | MX    | 3600 | 10 mail.domain.tld
| domain.tld        | TXT   | 3600 | "v=spf1 mx:mail.domain.tld -all"
| mail.domain.tld   | CNAME | 3600 | domain.tld
| _dmarc.domain.tld | TXT   | 3600 | "v=DMARC1; p=reject; pct=100; rua=mailto:reports@domain.tld"
| _imap.domain.tld  | SRV   | 3600 | 0 0 0 .
| _imaps.domain.tld | SRV   | 3600 | 0 1 993 mail.domain.tld
| _pop3.domain.tld  | SRV   | 3600 | 0 0 0 .
| _pop3s.domain.tld | SRV   | 3600 | 0 0 0 .

Role Variables
--------------

A description of the settable variables for this role should go here, including
any variables that are in defaults/main.yml, vars/main.yml, and any variables
that can/should be set via parameters to the role. Any variables that are read
from other roles and/or the global scope (ie. hostvars, group vars, etc.) should
be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in
regards to parameters that may need to be set for other roles, or variables that
are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: openbsd.mail, x: 42 }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a
website (HTML is not allowed).
