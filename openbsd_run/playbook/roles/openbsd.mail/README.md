openbsd.mail
=========

* https://man.openbsd.org/acme-client.1
* https://man.openbsd.org/openssl.1
* https://man.openbsd.org/pf.conf.5
* https://man.openbsd.org/smtpd.conf.5
* https://man.openbsd.org/spamd.conf.5

Requirements
---------

### DNS Records
| Host               | Type  | TTL  | Value |
| ------------------ | ----- | ---- | ----- |
| @                  | A     | 3600 | <IPv4 Address>
| @                  | AAAA  | 3600 | <IPv6 Address>
| @                  | MX    | 3600 | 10 mail.domain.tld.
| @                  | TXT   | 3600 | "v=spf1 mx:mail.domain.tld -all"
| default._domainkey | TXT   | 3600 | "k=rsa; p=<2048 key>"
| mail               | CNAME | 3600 | domain.tld
| _dmarc             | TXT   | 3600 | "v=DMARC1; p=reject; pct=100; rua=mailto:admin@domain.tld"
|                    | SRV   | 3600 | _imaps _tcp 0 1 993 mail.domain.tld.

* https://tools.ietf.org/html/rfc3501
* https://tools.ietf.org/html/rfc6376
* https://tools.ietf.org/html/rfc7489
