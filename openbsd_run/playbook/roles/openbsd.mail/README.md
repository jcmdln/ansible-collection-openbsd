openbsd.mail
=========
Setup a simple mail server using OpenSMTPD, spamd, Dovecot + SQLite.

Included in base:
* https://man.openbsd.org/acme-client.1
* https://man.openbsd.org/openssl.1
* https://man.openbsd.org/pf.4
* https://man.openbsd.org/pf.conf.5
* https://man.openbsd.org/smtpd.8
* https://man.openbsd.org/smtpd.conf.5
* https://man.openbsd.org/spamd.8
* https://man.openbsd.org/spamd.conf.5

Ports:
* https://www.dovecot.org/
* https://www.sqlite.org/


Requirements
---------

### DNS Records
* https://tools.ietf.org/html/rfc2181
* https://tools.ietf.org/html/rfc3501
* https://tools.ietf.org/html/rfc4035
* https://tools.ietf.org/html/rfc5452
* https://tools.ietf.org/html/rfc6186
* https://tools.ietf.org/html/rfc6376
* https://tools.ietf.org/html/rfc7489

| Host/Service          | Type  | TTL  | Value |
| --------------------- | ----- | ---- | ----- |
| @                     | MX    | 3600 | 10 mail.domain.tld.
| @                     | TXT   | 3600 | v=spf1 mx ~all
| _autodiscover._tcp    | SRV   | 3600 | 0  1  443  mail.domain.tld.
| _dmarc                | TXT   | 3600 | v=DMARC1; p=none; pct=100; rua=mailto:hostmaster@domain.tld
| _imaps._tcp           | SRV   | 3600 | 0  1  993  mail.domain.tld.
| _pop3s._tcp           | SRV   | 3600 | 10 1  995  mail.domain.tld.
| _submission._tcp      | SRV   | 3600 | 10 1  587  mail.domain.tld.
| _submissions._tcp     | SRV   | 3600 | 0  1  465  mail.domain.tld.
| <selector>._domainkey | TXT   | 3600 | v=DKIM1; k=rsa; p=<2048 key>
| mail                  | A     | 3600 | 1.2.3.4
| mail                  | AAAA  | 3600 | 2001:db8::1
