# openbsd.mail

Setup a simple mail server using OpenSMTPD, spamd, and Dovecot.

## About

In order to keep things simple this role uses real unix users each with their
own [Maildir](https://en.wikipedia.org/wiki/Maildir) rather than use virtual
users or duplicate where mail can end up by leaving an mbox around. Dovecot
only handles IMAP login and redelivering filtered mail by LMTP.

This may make things _too_ simple for some scenarios though the idea is that
you are giving trusted users unprivileged accounts by which they are afforded
system resources as well as a mailbox to get work done.

## Requirements

- Dovecot
  - https://www.dovecot.org
- OpenBSD
  - https://man.openbsd.org/acme-client.1
  - https://man.openbsd.org/openssl.1
  - https://man.openbsd.org/pf.4
  - https://man.openbsd.org/pf.conf.5
  - https://man.openbsd.org/smtpd.8
  - https://man.openbsd.org/smtpd.conf.5
  - https://man.openbsd.org/spamd.8
  - https://man.openbsd.org/spamd.conf.5

### DNS Records

The table below outlines which DNS records are required (or suggested):

[rfc5321]: https://datatracker.ietf.org/doc/html/rfc5321
[rfc6186]: https://datatracker.ietf.org/doc/html/rfc6186
[rfc6376]: https://datatracker.ietf.org/doc/html/rfc6376
[rfc7208]: https://datatracker.ietf.org/doc/html/rfc7208
[rfc7489]: https://datatracker.ietf.org/doc/html/rfc7489

| Host/Service          | Type  | TTL  | Value                                 |
| --------------------- | ----- | ---- | ------------------------------------- |
| @                     | A     | 3600 | 0.0.0.0                               |
| @                     | AAAA  | 3600 | ::1                                   |
| imap.domain.tld       | CNAME | 3600 | domain.tld                            |
| smtp.domain.tld       | CNAME | 3600 | domain.tld                            |
| [rfc5321]             |
| @                     | MX    | 3600 | 10 smtp.domain.tld.                   |
| [rfc6186]             |
| \_imap.\_tcp          | SRV   | 3600 | 0 1 143 imap.domain.tld.              |
| \_imaps.\_tcp         | SRV   | 3600 | 0 1 993 imap.domain.tld.              |
| \_submission.\_tcp    | SRV   | 3600 | 0 1 587 smtp.domain.tld.              |
| \_submissions.\_tcp   | SRV   | 3600 | 0 1 465 smtp.domain.tld.              |
| [rfc7208]             |
| @                     | TXT   | 3600 | v=spf1 mx -all                        |
| [rfc6376]             |
| $SELECTOR.\_domainkey | TXT   | 3600 | v=DKIM1; k=rsa; p=$RSA_PUBLIC_KEY     |
| [rfc7489]             |
| \_dmarc               | TXT   | 3600 | v=DMARC1; p=reject; pct=100; rf=afrf; |
|                       |       |      | rua=mailto:hostmaster@domain.tld;     |
|                       |       |      | ruf=mailto:hostmaster@domain.tld      |

#### DNSSEC

Consider enabling DNSSEC:

- https://datatracker.ietf.org/doc/html/rfc4035

## Sieve

- https://datatracker.ietf.org/doc/html/rfc5228
- https://datatracker.ietf.org/doc/html/rfc5233

### Examples

```perl
# ~/Mail/dovecot.sieve

require ["fileinto", "mailbox"];

if exists ["List-ID"] {
    if header :contains "List-ID" "alpinelinux.org" {
        if header :contains "List-ID" "~alpine/announce" {
            fileinto :create "alpine-announce";
        } elsif header :contains "List-ID" "~alpine/aports" {
            fileinto :create "alpine-aports";
        } elsif header :contains "List-ID" "~alpine/devel" {
            fileinto :create "alpine-devel";
        }
    } elsif header :contains "List-ID" "openbsd.org" {
        if header :contains "List-ID" "advocacy" {
            fileinto :create "openbsd-advocacy";
        } elsif header :contains "List-ID" "announce" {
            fileinto :create "openbsd-announce";
        } elsif header :contains "List-ID" "bugs" {
            fileinto :create "openbsd-bugs";
        } elsif header :contains "List-ID" "misc" {
            fileinto :create "openbsd-misc";
        } elsif header :contains "List-ID" "ports" {
            fileinto :create "openbsd-ports";
        } elsif header :contains "List-ID" "tech" {
            fileinto :create "openbsd-tech";
        }
    }
}
```

## Supplemental Reading

- [DOMAIN NAMES - CONCEPTS AND FACILITIES [1987]](https://datatracker.ietf.org/doc/html/rfc1034)
- [Simple Mail Transfer Protocol (2008)](https://datatracker.ietf.org/doc/html/rfc5321)
- [Internet Message Format [2008]](https://datatracker.ietf.org/doc/html/rfc5322)
- [Internet Message Access Protocol (IMAP) - Version 4rev2 [2021]](https://datatracker.ietf.org/doc/html/rfc9051)
