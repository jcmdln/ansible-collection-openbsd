# jcmdln.openbsd.mail

Setup a simple mail server using OpenSMTPD, Dovecot and Rspamd.

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
  - https://www.rspamd.com/
- OpenBSD
  - https://man.openbsd.org/acme-client.1
  - https://man.openbsd.org/openssl.1
  - https://man.openbsd.org/pf.4
  - https://man.openbsd.org/pf.conf.5
  - https://man.openbsd.org/smtpd.8
  - https://man.openbsd.org/smtpd.conf.5

### DNS Records

The table below outlines which DNS records are required (or suggested):

[rfc5321]: https://www.rfc-editor.org/rfc/rfc5321
[rfc6186]: https://www.rfc-editor.org/rfc/rfc6186
[rfc6376]: https://www.rfc-editor.org/rfc/rfc6376
[rfc7208]: https://www.rfc-editor.org/rfc/rfc7208
[rfc7489]: https://www.rfc-editor.org/rfc/rfc7489
[rfc8657]: https://www.rfc-editor.org/rfc/rfc8657

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

- https://www.rfc-editor.org/rfc/rfc4035

## Sieve

- https://www.rfc-editor.org/rfc/rfc5228
- https://www.rfc-editor.org/rfc/rfc5233

### Examples

```ruby
# ~/Mail/dovecot.sieve

require ["fileinto", "mailbox"];

if exists "list-id" {
	if header :contains "list-id" "alpinelinux.org" {
		if header :contains "list-id" "~alpine/announce" {
			fileinto :create "alpine-announce";
		} elsif header :contains "list-id" "~alpine/aports" {
			fileinto :create "alpine-aports";
		} elsif header :contains "list-id" "~alpine/devel" {
			fileinto :create "alpine-devel";
		}
	} elsif header :contains "list-id" "freelists.org" {
		if header :contains "list-id" "bootstrappable" {
			fileinto :create "bootstrappable";
		}
	} elsif header :contains "list-id" "openbsd.org" {
		if header :contains "list-id" "advocacy" {
			fileinto :create "openbsd-advocacy";
		} elsif header :contains "list-id" "announce" {
			fileinto :create "openbsd-announce";
		} elsif header :contains "list-id" "bugs" {
			fileinto :create "openbsd-bugs";
		} elsif header :contains "list-id" "misc" {
			fileinto :create "openbsd-misc";
		} elsif header :contains "list-id" "ports" {
			fileinto :create "openbsd-ports";
		} elsif header :contains "list-id" "tech" {
			fileinto :create "openbsd-tech";
		}
	}
}
```

## Supplemental Reading

- [DOMAIN NAMES - CONCEPTS AND FACILITIES [1987]](https://www.rfc-editor.org/rfc/rfc1034)
- [Simple Mail Transfer Protocol (2008)](https://www.rfc-editor.org/rfc/rfc5321)
- [Internet Message Format [2008]](https://www.rfc-editor.org/rfc/rfc5322)
- [Internet Message Access Protocol (IMAP) - Version 4rev2 [2021]](https://www.rfc-editor.org/rfc/rfc9051)
