openbsd.mail
=========

* https://man.openbsd.org/acme-client.1
* https://man.openbsd.org/openssl.1
* https://man.openbsd.org/pf.conf.5
* https://man.openbsd.org/smtpd.conf.5
* https://man.openbsd.org/spamd.conf.5
* https://www.dovecot.org/

Requirements
---------

### DNS Records
* https://tools.ietf.org/html/rfc3501
* https://tools.ietf.org/html/rfc6186
* https://tools.ietf.org/html/rfc6376
* https://tools.ietf.org/html/rfc7489

| Host               | Type  | TTL  | Value |
| ------------------ | ----- | ---- | ----- |
| @                  | A     | 3600 | <IPv4 Address>
| @                  | AAAA  | 3600 | <IPv6 Address>
| @                  | MX    | 3600 | 10 mail.domain.tld.
| @                  | TXT   | 3600 | "v=spf1 mx:mail.domain.tld -all"
| default._domainkey | TXT   | 3600 | "k=rsa; p=<2048 key>"
| mail               | CNAME | 3600 | domain.tld
| _dmarc             | TXT   | 3600 | "v=DMARC1; p=reject; pct=100; rua=mailto:admin@domain.tld"
| _imap._tcp         | SRV   | 3600 | 0  0  0    .
| _imaps._tcp        | SRV   | 3600 | 0  1  993  mail.domain.tld.
| _pop3._tcp         | SRV   | 3600 | 0  0  0    .
| _pop3s._tcp        | SRV   | 3600 | 10 1  995  mail.domain.tld.
| _submission._tcp   | SRV   | 3600 | 0  0  0    .
| _submissions._tcp  | SRV   | 3600 | 0  1  465  mail.domain.tld.
