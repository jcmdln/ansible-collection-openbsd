openbsd.mail
=========
Setup a simple mail server using OpenSMTPD, spamd, and Dovecot.

About
----------
In order to keep things simple, this role associates a [Maildir]() with real
unix users rather than virtual users. Dovecot only handles IMAP login and
redelivering filtered mail by LMTP.

This may make things _too_ simple for some scenarios though the idea is that
you are giving trusted users unprivileged accounts by which they are afforded
system resources as well as a mailbox to get work done.


Requirements
---------
* https://man.openbsd.org/acme-client.1
* https://man.openbsd.org/openssl.1
* https://man.openbsd.org/pf.4
* https://man.openbsd.org/pf.conf.5
* https://man.openbsd.org/smtpd.8
* https://man.openbsd.org/smtpd.conf.5
* https://man.openbsd.org/spamd.8
* https://man.openbsd.org/spamd.conf.5
* https://www.dovecot.org/

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
| @                     | TXT   | 3600 | v=spf1 mx -all
| _autodiscover._tcp    | SRV   | 3600 | 0  1  443  mail.domain.tld.
| _dmarc                | TXT   | 3600 | v=DMARC1; p=reject; pct=100; rua=mailto:hostmaster@domain.tld
| _imaps._tcp           | SRV   | 3600 | 0  1  993  mail.domain.tld.
| _submission._tcp      | SRV   | 3600 | 10 1  587  mail.domain.tld.
| _submissions._tcp     | SRV   | 3600 | 0  1  465  mail.domain.tld.
| <selector>._domainkey | TXT   | 3600 | v=DKIM1; k=rsa; p=<2048 key>
| mail                  | A     | 3600 | 1.2.3.4
| mail                  | AAAA  | 3600 | 2001:db8::1

### User Sieve Example
Below is an example of filtering OpenBSD Mailing lists:

```sieve
# ~/Mail/dovecot.sieve

require ["fileinto", "mailbox"];

if anyof (header "Precedence" "list", header "Precedence" "bulk", exists "List-Id") {
  if header :contains "List-Id" "advocacy@openbsd.org" {
    fileinto :create "OpenBSD/advocacy";
  } elsif header :contains "List-Id" "announce@openbsd.org" {
    fileinto :create "OpenBSD/announce";
  } elsif header :contains "List-Id" "bugs@openbsd.org" {
    fileinto :create "OpenBSD/bugs";
  } elsif header :contains "List-Id" "misc@openbsd.org" {
    fileinto :create "OpenBSD/misc";
  } elsif header :contains "List-Id" "ports@openbsd.org" {
    fileinto :create "OpenBSD/ports";
  } elsif header :contains "List-Id" "tech@openbsd.org" {
    fileinto :create "OpenBSD/tech";
  }
}
```
