# System Security — Session 3: Scanning

---

## Why Does This Matter?

Two core questions for any defender:

1. **Are there unknown hosts on our network?** — rogue devices, forgotten test servers, planted hardware
2. **Are there unknown/unnecessary services on our servers?** — every open port is a potential entry point

If your users can reach a service → an external attacker can too.

**Rule:** never connect a new server to a live network before it is properly configured and hardened.
> A new unprotected server exposed to the internet gets compromised within ~10 minutes.

---

## Simple Vulnerability Assessment

**The defender's workflow:**

1. Scan the network → find all hosts → compare against what *should* be there
2. Scan each host → find all open ports/services → compare against what *should* be running
3. Investigate, close, remove anything unexpected

This is **not** offensive penetration testing — it's checking that reality matches the plan.

---

## Nmap

**Nmap** (Network Mapper) is the standard tool for host discovery and port scanning.

### Install

```bash
# Quick install (may be slightly older version)
sudo apt install nmap

# Install from source (recommended — latest version, integrity verified)
sudo apt-get install build-essential
wget https://nmap.org/dist/nmap-7.95.tar.bz2

# Verify integrity before installing
md5sum nmap-7.95.tar.bz2          # compare against hash on nmap.org
# or use GPG with signed hashes

# Unpack, compile, install
bzip2 -cd nmap-7.95.tar.bz2 | tar xvf -
cd nmap-7.95/
./configure
make
sudo make install

# Verify
nmap --version
```

**Why install from source?** You get the latest version with all current signatures and security fixes, and you can verify integrity yourself before installing.

---

## Scanning Hosts (Host Discovery)

Goal: find all live hosts on a network segment.

```bash
nmap -h                                        # help / all options

# Ping scan — no port scan, just find live hosts
nmap -vv -sn 192.168.1.1-100                  # scan a range
nmap -vv -sn 192.168.1.0/24                   # scan entire subnet

# Faster scan (reduce timeout, aggressive timing)
nmap -vv -n -sn --max-rtt-timeout 300ms 192.168.1.0/24 -T4
```

**Flag reference:**

| Flag | Meaning |
|---|---|
| `-vv` | very verbose output |
| `-sn` | ping scan only — no port scan |
| `-n` | no DNS resolution (faster) |
| `-T4` | aggressive timing (faster, noisier) |
| `--max-rtt-timeout 300ms` | cut off slow responses |

---

## Scanning Services (Port Scanning)

Goal: find which services/applications are running on a host.

```bash
# TCP SYN scan — fast, less noisy than full connect
nmap -vv -sS 192.168.1.0/24

# Scan for a specific port (e.g. FTP on 21)
nmap -vv -sS -n -Pn -p 21 192.168.1.0/24 -T4 -oG - | grep 'open'

# Common ports to check
nmap -p 22 192.168.1.0/24       # SSH
nmap -p 80,443,8080 192.168.1.0/24  # HTTP/HTTPS
nmap -p 3306 192.168.1.0/24    # MySQL
nmap -p 21 192.168.1.0/24      # FTP

# OS detection
nmap -vv -O 192.168.1.100-110

# Service/version detection
nmap -vv -sV 192.168.1.100-110
```

**Flag reference:**

| Flag | Meaning |
|---|---|
| `-sS` | TCP SYN scan (stealth scan) |
| `-sV` | detect service version |
| `-O` | OS detection |
| `-Pn` | skip host discovery — treat all hosts as up |
| `-p PORT` | scan specific port(s) |
| `-oG -` | grepable output to stdout |

---

## Hosts vs Services — What's More Dangerous?

| Scenario | Risk level | Why |
|---|---|---|
| Unknown host — employee's personal laptop | Medium | Policy violation, unmanaged device |
| Unknown host — planted by attacker | High | Direct threat, possible data exfil |
| Forgotten host (old test server) | High | Unpatched, no one monitoring it |
| Unnecessary service on a server | High | Unmonitored attack surface, may have unpatched CVEs |

**Key point:** every open port = an application listening for connections = a potential vulnerability. If the service isn't needed, close it.

---

## Exercises — Session 3

**3.a — Install/update Nmap:**
```bash
nmap --version           # check current version
# If outdated, install from source as above
# Always verify integrity of the download first
```

**3.b — Scan hosts on your home network:**
```bash
nmap -vv -sn 192.168.1.0/24              # find all hosts
nmap -vv -O 192.168.1.0/24              # try to detect OS
```
- Turn on all devices first (TV, smart lights, speakers) — they all show up
- Note down every host found and what you think it is
- Anything unexpected?

**3.c — Scan services on your own machine:**
```bash
nmap -vv -sV localhost                   # scan your own host
nmap -vv -sV 192.168.1.X                # scan another device
```
- For each open port: what is the service? Do you need it?
- Google the service name + "vulnerabilities" or "CVE"
- How would you stop a service you don't need?
  ```bash
  sudo systemctl stop servicename
  sudo systemctl disable servicename
  ```
- When should you do this? → Every new server before it goes into production

---

## Key Concepts for Exam

- **Open port = running service = attack surface** — every unnecessary service is unnecessary risk
- **Defenders scan too** — port scanning isn't just for attackers; it's how admins verify reality matches policy
- **Nmap does two things:** host discovery (`-sn`) and port/service scanning (`-sS`, `-sV`, `-O`)
- **Never expose an unconfigured server** — attackers find it within minutes
- **Verify download integrity** before installing security tools (md5sum / GPG)
- **The defender's mindset:** does reality match the plan? If not — investigate and fix