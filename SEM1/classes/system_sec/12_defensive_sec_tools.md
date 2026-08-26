# System Security — Session 12
## Defensive Security Tools: sXID · Tripwire · PortSentry · Squid · Shorewall

---

## The Big Picture

This session is about **host-based and network-based detection and prevention** — tools that watch for intrusions, scan attempts, and policy violations. These are all **defensive** tools — they don't stop an attacker getting in, but they detect when something has changed or is being probed, and can react automatically.

---

## File Permissions — The Fine Print: SUID & SGID

### The problem with `/etc/shadow`

Normal users cannot read or write `/etc/shadow` — it's owned by root. But users need to be able to change their own password with `passwd`. How does that work if they can't write to shadow?

**Answer: SUID (Set User ID upon execution)**

---

## SUID & SGID

| Permission | What it does |
|---|---|
| **SUID** (Set User ID) | When a file is executed, it runs with the **file owner's** permissions, not the executing user's permissions |
| **SGID** (Set Group ID) | Same idea but for group — runs with the **file's group** permissions |

**Example:** `/usr/bin/passwd` is owned by root and has SUID set. When any user runs it, it executes as root — which is why it can write to `/etc/shadow`.

```bash
ls -l /usr/bin/passwd
# -rwsr-xr-x  root root  ...
#    ^ the 's' here = SUID is set
```

The `s` replaces the `x` in the owner execute position.

### Why SUID changes are a security risk

- If an attacker sets SUID on a shell or script they own → anyone who runs it gets root
- A rootkit will set SUID on backdoor files to maintain persistent root access
- An unexpected SUID file = strong indicator of compromise

### Finding SUID files
```bash
sudo find /usr -perm -4000               # find files with SUID bit set
sudo find /usr -perm -4000 -exec ls -l {} \;   # with full details
sudo find / -perm -4000 2>/dev/null      # whole system (suppress permission errors)
```

### Setting SUID manually
```bash
chmod u+s somefile      # symbolic
chmod 4755 somefile     # octal — the 4 prefix sets SUID
```

---

## sXID — Monitoring SUID/SGID Changes

sXID is a tool that **scans specified directories for SUID/SGID files** and alerts you when anything changes — a new SUID file appears, or an existing one loses its SUID bit.

```bash
sudo apt-get install sxid
```

### Configuration: `/etc/sxid.conf`

| Setting | Purpose |
|---|---|
| `EMAIL` | Who to email reports to |
| `KEEP_LOGS` | How many old logs to retain |
| `SEARCH` | Space-separated list of directories to scan |
| `EXCLUDE` | Directories to ignore |

### Running manually
```bash
sudo sxid -n       # -n = dry run / spot check, don't update DB
sudo sxid          # run normally and update the DB
```

### Automating with cron
```bash
sudo crontab -e
# Run every hour:
0 * * * * /usr/sbin/sxid
```

---

## Tripwire — File Integrity Monitoring

### The problem

An attacker or rootkit that has root access will:
- Replace system binaries (`ls`, `passwd`, `login`) with trojaned versions
- Modify config files to maintain access
- **Reset timestamps and falsify file sizes** to hide changes — `ls -l` will show nothing unusual

### How Tripwire solves this

Tripwire calculates a **cryptographic hash** of each monitored file and stores it in a private database. Later it recalculates the hash — if it has changed, the file has been modified, regardless of what `ls` shows.

A hash cannot be faked without knowing the original content — and the DB itself is protected with a passphrase.

```
File → SHA hash → stored in Tripwire DB
Later: File → new SHA hash → compare → MATCH or CHANGE
```

### Install and setup
```bash
sudo apt-get install tripwire
# During install: set site passphrase and local passphrase
```

### Key commands
```bash
sudo tripwire --init                    # initialise the database (baseline)
sudo tripwire --check                   # run integrity check against DB
sudo tripwire --update --twrfile report.twr   # update DB after approved changes
```

### Configuration
- Policy file defines **which directories/files** to monitor and what properties to check
- Common monitored paths: `/etc`, `/bin`, `/usr/bin`, `/sbin`, `/lib`
- Docs/examples: https://linuxconfig.org/intrusion-detection-systems-using-tripwire-on-linux

### Alternatives to Tripwire
| Tool | Notes |
|---|---|
| **AIDE** | Open source, simpler config, popular on Debian/Ubuntu |
| **iNotify** | Linux kernel mechanism — real-time file change events |
| **kQueue** | BSD equivalent of iNotify |

---

## PortSentry — Port Scan Detection & Reaction

### The problem

Before an attacker exploits a service, they **scan** to find what's open. If you can detect the scan, you can react before the actual attack.

### What PortSentry does

- Listens on ports you define (including fake ports that nothing real listens on)
- When a connection attempt is made to a watched port → **that's a scan**
- Can react automatically: block the source IP in iptables, or make ports appear in different states

```bash
sudo apt-get install portsentry
```

### Configuration: `/etc/portsentry/portsentry.conf`

Key settings:
```
# Ports to watch (fake ports — nothing real should be on these)
TCP_PORTS="1,7,9,11,15,70,79"
UDP_PORTS="1,7,9,69,161,162"

# Block the scanner in iptables (uncomment this line):
KILL_ROUTE="/sbin/iptables -I INPUT -s $TARGET$ -j DROP"
```

### Why uncomment the iptables block rule?
Without it, PortSentry just logs the scan but does nothing. The block rule makes PortSentry actively drop all further traffic from the scanner — turning detection into prevention.

### Effect on nmap scans
- Before PortSentry: nmap sees open/closed/filtered ports honestly
- After PortSentry + iptables rule: scanner gets blocked after first probe → scan appears incomplete or all ports filtered
- You control your **"radar profile"** — what attackers see when they scan you

---

## Squid Proxy

Squid is a **web proxy** — it sits between clients and the internet, forwarding and optionally filtering web traffic.

### What it can do

| Feature | Use |
|---|---|
| **Caching** | Store frequently accessed content locally → faster browsing, less bandwidth |
| **Content filtering** | Block traffic by domain, URL, or content keywords |
| **Protocol support** | HTTP, HTTPS, FTP, SSL, TLS |
| **Direction** | Can proxy outbound (clients → internet) or inbound (internet → your servers) |

### Security uses

- Block access to specific countries/domains (`.ru`, `.cn`, etc.)
- Block SQL injection strings (`drop table`, `insert into`) in outbound requests
- Block keywords (`Sverige`, `confidential`) to prevent data exfiltration
- Force all web traffic through the proxy at the gateway — no bypassing

### Configuration: `/etc/squid/squid.conf`

```
# Block by domain:
acl blocked_domains dstdomain .ru .se .ch
http_access deny blocked_domains

# Block by content keyword:
acl bad_words url_regex -i "Sverige" "Sweden"
http_access deny bad_words
```

### Why block `drop table` and `insert`?
These are SQL keywords. If outbound web requests contain them, it could indicate:
- A web form sending user input directly to a backend unsanitised (SQL injection attempt)
- Data being exfiltrated via URL parameters
Blocking them at the proxy adds a network-level layer of SQL injection prevention.

---

## Shorewall — Gateway Firewall Configuration

Shorewall is a **configuration layer on top of iptables** that makes it easier to set up a multi-zone network gateway firewall.

### The problem with raw iptables

iptables rules are powerful but verbose and hard to read. A gateway with 3 interfaces needs dozens of rules — easy to get wrong.

### Shorewall's approach

Organise the network into **zones** and write rules in terms of zones, not interfaces:

| Zone | Represents |
|---|---|
| `net` | The external internet |
| `dmz` | Servers exposed to the internet (web, mail) |
| `loc` | Internal company intranet |

### Typical gateway firewall policy

```
Internet → DMZ:     Allow HTTP/HTTPS only (to web server)
Internet → Intranet: Block everything
DMZ → Intranet:     Block everything (except established connections)
Intranet → Internet: Allow (users browse the web)
Intranet → DMZ:     Allow (internal staff access internal servers)
```

This isolates the DMZ — even if a web server is compromised, the attacker can't reach the intranet directly.

---

## Exam Key Concepts

- **SUID** = file runs as its owner's UID, not the runner's — necessary for `passwd` to write `/etc/shadow`
- **SUID risk** = if an attacker sets SUID on a shell → instant root for anyone who runs it
- **sXID** = monitors which files have SUID/SGID set and alerts on changes
- **Tripwire** = file integrity monitoring using hashes — detects changes even if timestamps are faked
- **Hash-based integrity** = the only reliable way to detect file tampering (timestamps can be forged, hashes cannot without changing content)
- **PortSentry** = detects port scans and can block the source IP automatically via iptables
- **Radar profile** = what an attacker sees when they scan you — PortSentry lets you control this
- **Squid** = web proxy for filtering outbound/inbound traffic by domain or content
- **Blocking SQL keywords** = network-level SQL injection defence at the proxy
- **Shorewall** = human-readable iptables config using network zones (net/dmz/loc)
- **DMZ** = isolated network segment for public-facing servers — compromising them doesn't give access to the intranet