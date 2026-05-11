# System Security — The WHYs
### All sessions, all themes — why we learn them, why they matter

---

## Session 1 — Security Policies

### Why do we have security policies?
- Technology alone cannot protect a company — humans make mistakes
- A policy defines *expected behaviour* so people know what is allowed and what isn't
- Without a policy, you cannot hold employees accountable for bad behaviour
- Regulators (GDPR, NIS2) **require** documented policies — no policy = legal liability

### Why use frameworks (ISO 27001, NIST, CIS Controls)?
- You don't have to invent security from scratch — smarter people already did
- Frameworks are battle-tested across thousands of companies
- They give you a **checklist** — hard to miss something important
- Some clients and contracts **require** you to follow a specific framework

### Why is user awareness the most important policy?
- 85–95% of all breaches start with a human clicking something they shouldn't
- No technical control can fully stop a human being tricked
- Training is the only effective defence against phishing and social engineering

### Why is insurance relevant to security?
- M&S cyberattack (2025): £136M loss, £100M insured → £36M direct loss
- Without insurance a single attack can bankrupt a company
- Insurance also incentivises good security (lower premiums for better posture)

---

## Session 2 — Disk Encryption & Sudo

### Why encrypt disks (LUKS)?
- OS access controls (passwords, permissions) only work if the OS is running
- An attacker with **physical access** can boot from USB and bypass all OS controls
- With disk encryption, the data is unreadable without the key — even if the disk is stolen
- All company laptops and servers should be encrypted — **physical theft is common**

### Why not just use a strong login password?
- A password only protects the running OS
- A stolen laptop = attacker boots their own OS = your password is irrelevant
- Encryption protects **the data itself**, not just the session

### Why use sudo instead of sharing root?
- Root can do **anything** — no restrictions, no audit trail
- Sharing root = no accountability (who deleted that file?)
- `sudo` gives controlled, logged, time-limited privilege escalation
- If one account is compromised, the attacker still can't do everything

### Why use privilege separation (least privilege)?
- Every user/process should only have the access they **actually need**
- If an account is compromised, the blast radius is limited
- A network operator doesn't need to reboot servers — so don't give them that permission
- This is called **Principle of Least Privilege** — foundational security concept

### Why use `visudo` and never edit sudoers directly?
- A syntax error in `/etc/sudoers` can **lock everyone out of sudo** permanently
- `visudo` validates syntax before saving — it catches mistakes before they break things

---

## Session 2.5 — Filesystem & Permissions

### Why does Linux have a standard filesystem hierarchy?
- Consistency across all Linux systems — you always know where config files are (`/etc`), logs (`/var/log`), binaries (`/bin`)
- Makes administration and forensics predictable
- A security analyst on any Linux system knows where to look

### Why do file permissions matter for security?
- If any user can read `/etc/shadow` — attacker gets all password hashes
- If any user can write to `/bin/` — attacker can replace system commands with malicious ones
- Permissions are the OS's primary access control mechanism
- Wrong permissions = privilege escalation opportunities

### Why is execute permission on a directory different from a file?
- On a **file**: allows running it as a program
- On a **directory**: allows entering it (`cd`) and accessing its contents
- Removing execute from a directory blocks access even if the user can read the listing

---

## Session 3 — Scanning (Nmap)

### Why scan your own network?
- You cannot defend what you don't know exists
- Rogue devices, forgotten test servers, unauthorised hardware — all invisible without scanning
- Every open port is a potential entry point — you need to know what's open

### Why is a defender scanning their own network legitimate?
- It's your network — you're responsible for what's on it
- Attackers will scan it anyway — better you find problems before they do
- Regular scanning is a core part of vulnerability management

### Why install Nmap from source instead of apt?
- `apt` gives you an older, packaged version
- Source gives you the **latest version** with the newest vulnerability signatures and features
- For security tools, being up to date matters

### Why is a service running on a server a security risk?
- Every service is software → software has bugs → bugs can be exploited
- A service you don't need = unnecessary attack surface
- Rule: **disable everything you don't use**

### Why should you never connect a new server to a live network before hardening it?
- Default configs are designed for convenience, not security
- A fresh Ubuntu install has several services running that may not be needed
- Attackers scan continuously — a new unprotected server can be compromised within minutes of going online

---

## Session 4 — Understanding Attacks (Metasploit)

### Why do defenders study attacks?
- To understand what you're defending against
- Every defence decision maps to a specific attack vector
- "Know your enemy" — if you don't know how something is attacked, you can't defend it
- You need to think like an attacker to find your own weaknesses first

### Why do old vulnerabilities still work?
- A vulnerability exists as long as the software is **unpatched**
- Age is irrelevant — a 2012 vulnerability in unpatched software is just as exploitable today
- Many companies run legacy systems that can never be patched (cost, compatibility)
- This is why **patching is the #1 technical defence**

### Why does Metasploit matter?
- It shows that exploitation is **not magic** — it's a structured, repeatable process
- The workflow is always the same: `search` → `use` → `set options` → `exploit`
- Understanding the tool helps you understand what an attacker can do in minutes

### Why is patching the most important technical defence?
- Most exploits target **known** vulnerabilities with published CVEs
- A patched system has no known attack surface for those exploits
- Unpatched = known weakness that any attacker with Metasploit can exploit automatically

### Why is phishing the #1 attack vector?
- Technical defences (firewalls, patching) protect the perimeter
- Phishing bypasses all of that by targeting humans directly
- Once a user clicks, malware runs **inside** the network — behind all perimeter defences
- The attacker now has a foothold from inside, where internal systems have no protection

---

## Session 5 — File Permissions & ACL

### Why are standard Linux permissions sometimes not enough?
- Standard permissions allow only: one owner, one group, one "others" setting
- Real companies need: group A gets read, group B gets read+write, user C gets write, everyone else nothing
- Standard permissions can't express this — ACL can

### Why use ACL (Access Control Lists)?
- Fine-grained control: assign specific permissions to **any number** of users and groups
- Example: lotte gets write access independently of her group membership
- Useful for shared project folders, departmental resources, sensitive files
- Standard permissions are a blunt instrument — ACL is precise

### Why set **default** ACL (`d:`) on a directory?
- Without default ACL, new files created inside the directory don't inherit the rules
- This creates a security gap: new file = open access until manually fixed
- Default ACL ensures every new file automatically gets the correct permissions
- Prevents accidental exposure of newly created sensitive files

### Why is the order of ACL rules important?
- The most specific rule wins — user rule > group rule > others
- If lotte is also in salg group, her user rule overrides the group rule
- Understanding this prevents unintended permission grants

---

## Session 6 — LDAP & Central Authentication

### Why centralise user management?
- Without it: every server and every laptop has its own local user list
- Adding/removing an employee means updating every machine individually
- Easy to miss one — a fired employee might still have access to one forgotten server
- Central management = one change applies everywhere instantly

### Why is LDAP used for this?
- LDAP is a standardised, open protocol — works with Linux, Windows, macOS, and most applications
- It's the foundation of **Active Directory** (Microsoft's enterprise directory)
- Many services (SSH, email, web apps) can authenticate against LDAP natively
- One user database → consistent access control across all systems

### Why separate **authentication** and **authorisation**?
- **Authentication** = proving who you are (LDAP handles this)
- **Authorisation** = what you're allowed to do (can be separate, e.g. ACL, group membership)
- Keeping them separate allows flexible, layered access control
- You can authenticate centrally but authorise locally per service

### Why use high UID/GID numbers for LDAP users?
- Local Linux users typically get UIDs 1000–1999
- If LDAP users have the same UIDs, there are **collisions** — system gets confused
- High numbers (10000+) guarantee no conflict with local accounts

### Why is LDAP a risk if not encrypted?
- By default, LDAP traffic is **plaintext** — credentials sent over the network unencrypted
- An attacker on the same network can sniff usernames and passwords
- Solution: **LDAPS** (LDAP over TLS) encrypts the connection
- This is why TLS matters even on internal networks

---

## Session 7 — User Login Control & PAM

### Why disable a user's login instead of deleting them?
- Deleting removes audit trail — you lose the history of what they did
- Files owned by deleted users become orphaned (owned by phantom UID)
- Disabling is reversible — if it was a mistake, you can re-enable
- Useful during investigations, leave of absence, or HR disputes

### Why lock an account vs. remove the shell?
- **Remove shell** (`nologin`): user can't get a terminal, but services might still work under that account
- **Lock account** (`passwd -l` or `usermod -L`): blocks all password-based login completely
- Different tools for different situations — depends on what you want to block

### Why monitor user activity (`acct`)?
- Know what commands users are running on your systems
- Detect suspicious behaviour — e.g. a user running `nmap` or `cat /etc/shadow`
- Provides an audit trail for forensic investigation after an incident
- Required by many compliance frameworks (ISO 27001, NIS2)

### Why is 2FA better than a strong password alone?
- A password can be stolen without the user knowing (phishing, keylogger, breach)
- 2FA requires something the attacker **also has to physically steal**
- Two passwords is NOT 2FA — they're the same factor (both "something you know")
- True 2FA = two different factor types (e.g. password + phone app)

### Why is a physical token better than a software token?
- Software tokens (app on phone) can be copied digitally if the phone is compromised
- Specialised hardware tokens (YubiKey, etc.) are purpose-built and very hard to clone
- Physical theft is required — and the user notices immediately when their token is gone
- The harder and more physical the theft, the lower the attacker's success rate

### Why use PAM (Pluggable Authentication Module)?
- Linux needs a flexible system to handle different authentication methods
- PAM allows mixing and stacking: password AND USB token AND TOTP app
- New authentication methods can be added without rewriting applications
- One config layer controls auth for all PAM-aware services (SSH, login, sudo, etc.)

---

## Session 8 — Remote Authentication & SSH

### Why is remote login a security risk?
- Exposes authentication to the internet — attackers can try to log in from anywhere
- Default configs are often too permissive (root login allowed, standard port, all users)
- Every exposed service is a potential entry point

### Why change the default SSH port (22)?
- Automated scanners and bots **constantly** scan port 22 for SSH services
- Moving to a non-standard port (e.g. 22123) drops off most automated attack traffic
- It's **security through obscurity** — not a real defence alone, but reduces noise
- Gives you cleaner logs and fewer brute force attempts to deal with

### Why disable root login over SSH?
- If an attacker brutes SSH and root login is allowed → immediate full system access
- With root disabled, they'd need to compromise a normal user first, then escalate
- Adds an extra step to the attack chain — more time for detection
- Ubuntu default is `prohibit-password` — always verify, never assume

### Why restrict SSH to specific users/groups?
- **Least privilege** — only people who need SSH access should have it
- Reduces the attack surface: fewer accounts = fewer targets to brute force
- If a user's credentials are stolen, they can't SSH in if they're not in `AllowUsers`
- Think: should an HR employee be able to SSH into the billing server? No.

### Why use public/private key authentication instead of passwords?
- A password can be guessed, phished, or brute forced
- A 256-bit private key has ~10⁷⁵ possible combinations — **impossible to brute force**
- The key is never transmitted — only proof-of-possession is verified
- Attacker needs **physical access** to the client machine to steal the key file

### Why is the public key safe to share/copy?
- Asymmetric cryptography: what one key encrypts, only the other can decrypt
- The public key can only **verify** — it cannot log you in
- Even if an attacker copies your public key, they still need the private key to authenticate
- Sharing the public key is the intended design — that's why it's called "public"

### Why add a passphrase to a private key?
- If your laptop is stolen, the attacker now has your private key file
- Without a passphrase, they can use it immediately
- With a passphrase: they need the file **AND** the passphrase → true 2FA
- Something you **have** (the key file) + something you **know** (the passphrase)

### Why disable password authentication once keys are set up?
- As long as password login is enabled, brute force is still possible
- Disabling it means **only key holders can log in** — no password = no brute force
- This is the gold standard for SSH security in production environments

### Why is key-based login "something you have" not "something you know"?
- You don't memorise the private key — you possess the file
- The key is 256 bits of random data — not derived from memory
- It's categorically a possession factor, same as a USB token or smart card
- This is important for the 2FA discussion — key alone = 1 factor, key + passphrase = 2 factors

---

## Session 9 — Secure File Transfer & Kerberos

### Why not just use FTP to transfer files?
- FTP sends everything in **plaintext** — filename, contents, and credentials are all visible on the network
- Anyone with a packet sniffer (Wireshark, tcpdump) on the same network sees all of it
- In the lab: you can verify SCP is encrypted by capturing the traffic — you see nothing readable
- Plaintext protocols have no place in a company environment

### Why use SCP vs. SFTP — isn't it the same?
- Both are encrypted and both use SSH underneath — that part is the same
- **SCP** = single command, non-interactive, just copies a file or directory
- **SFTP** = interactive session, like a terminal but for files — browse, upload, download, delete
- SCP is better for scripting and automation; SFTP is better when you need to explore or manage files
- Neither is "safer" — the choice is about workflow, not security level

### Why does Kerberos exist if we already have LDAP?
- LDAP authenticates you but still requires sending credentials to the service you're accessing
- Kerberos solves the "how do you prove who you are **without sending your password**" problem
- Every service in a Kerberos environment trusts the KDC — not each other
- You authenticate **once**, get a ticket, and use that ticket everywhere — true Single Sign-On

### Why is a ticket system more secure than sending passwords?
- A password is a **shared secret** — both sides have to know it, and it can be stolen in transit
- A Kerberos ticket is time-limited, service-specific, and encrypted — useless outside its context
- Even if a ticket is intercepted, it only works for one service and expires quickly
- The actual password **never leaves the client machine** — it's only used locally to decrypt the TGT

### Why does Kerberos need time synchronisation (NTP)?
- Tickets contain timestamps — they're only valid for a short window (typically 5–10 minutes)
- If client and server clocks are out of sync, valid tickets get rejected
- This is a deliberate design choice — it limits how long a stolen ticket is usable
- NTP (Network Time Protocol) keeps all machines synchronised — Kerberos depends on it

### Why is Kerberos the foundation of Windows Active Directory?
- Every Windows domain login uses Kerberos under the hood
- LDAP handles the directory (who exists, what groups they're in)
- Kerberos handles authentication (proving who you are without sending passwords)
- Understanding Kerberos = understanding enterprise authentication in almost every large organisation

---

## Session 11 — Host Firewall (iptables)

### Why does a server need its own firewall if there's already a network firewall?
- A network firewall protects the **perimeter** — traffic coming from outside
- Once an attacker is inside the network (phishing, compromised workstation), the network firewall doesn't help
- A **host firewall** (iptables) protects the individual server from other machines on the same internal network
- Defence-in-depth: multiple layers means one failure doesn't expose everything

### Why use iptables and not just close ports by stopping services?
- Stopping a service removes the port, yes — but what if a service needs to run but only be accessible to specific IPs?
- iptables lets you say: "this port is open, but **only** from 192.168.1.0/24"
- That granularity is impossible with just starting/stopping services
- Also: iptables blocks traffic before it reaches the service — even less attack surface

### Why is rule order critical in iptables?
- iptables evaluates rules **top-down** and stops at the first match
- If you put a broad ACCEPT rule before a specific DROP rule, the DROP never fires
- Example: `ACCEPT all` before `DROP port 22 from 10.0.0.5` — the drop never executes
- This is the same principle as firewall rule ordering in network firewalls

### Why set a default DENY (DROP) policy instead of default ALLOW?
- Default ALLOW = everything gets through unless explicitly blocked — you have to know every threat in advance
- Default DENY = nothing gets through unless explicitly allowed — you control everything
- Default DENY is much harder to misconfigure dangerously — unknown traffic gets blocked automatically
- Standard hardening practice: **whitelist, don't blacklist**

### Why use DROP instead of REJECT?
- **REJECT** sends an error back: "connection refused" — the attacker knows the port is there but filtered
- **DROP** gives no response — the attacker doesn't know if the host exists, the port is closed, or the packet was dropped
- DROP is quieter and gives less information to an attacker
- Trade-off: legitimate users also get no error feedback — may look like a network problem

### Why give servers static IP addresses (not DHCP)?
- iptables rules reference IP addresses — if a server's IP changes, the rules break
- Services that other machines connect to need a **predictable, permanent address**
- DHCP is for user machines that move around; servers stay put
- Also: static IP = easier to audit, monitor, and troubleshoot

---

## Session 12 — Defensive Security Tools

### Why use Tripwire (file integrity monitoring)?
- An attacker who gains access will modify files — install backdoors, change configs, replace binaries
- Tripwire creates a **cryptographic baseline** of your system before any compromise
- After a suspected incident, run Tripwire — it tells you exactly which files changed and when
- Without FIM, you're guessing what the attacker touched — with it, you know
- Connects to the **Integrity** part of CIA — protecting files from unauthorised change

### Why run Tripwire on a clean system before connecting to a network?
- The baseline must represent a **known-good state**
- If you baseline after a compromise, the malicious changes are baked in as "normal"
- Rule: establish baseline immediately after install, before any network exposure
- This is also why installation media integrity (Session 1) matters — start clean

### Why use sXID to monitor SUID/SGID files?
- SUID files run with the **owner's permissions**, not the caller's — usually root
- If an attacker can create or modify a SUID root file, they get instant root access
- sXID tracks which SUID/SGID files exist and alerts when new ones appear
- A new SUID file appearing on a server is a major red flag — possible rootkit or backdoor

### Why use PortSentry (port scan detection)?
- A port scan is almost always the **reconnaissance phase** before an attack
- If you detect a scan early, you can block the scanner before they find an exploitable service
- PortSentry can automatically add firewall rules to block the scanning IP
- It's an early warning system — detecting attacker intent before they act

### Why use a proxy (Squid) as a security tool?
- All outbound web traffic goes through the proxy — one place to log and filter everything
- You can block malicious domains, C2 (command and control) servers, or specific categories
- If malware infects a machine and tries to "phone home", the proxy can block it
- Logs reveal which machines are making unusual requests — good for incident detection

### Why use Shorewall instead of raw iptables commands?
- iptables syntax is complex — it's easy to make mistakes that silently open security holes
- Shorewall provides a higher-level config language that generates iptables rules correctly
- Easier to audit: the Shorewall config is readable, iptables rules are not
- Same principle as using `visudo` instead of editing sudoers directly — safer tooling reduces errors

---

## Session 13 — System Infection

### Why study malware types if this is a defenders' course?
- You can only defend against threats you understand
- Each malware type requires different prevention, detection, and recovery strategies
- A ransomware response is completely different from a rootkit response
- "Know your enemy" applies here too — the defender must know what infection looks like

### Why are rootkits the most dangerous type of malware?
- A rootkit modifies the **OS itself** — the kernel, system calls, process listings
- Once installed, the infected OS actively lies to you: `ps` won't show the malicious process, `ls` won't show the hidden files
- You cannot trust **any output** from a compromised system
- Detection requires booting from a **trusted external source** — an uninfected live USB
- This is exactly why baseline tools like Tripwire must be run from outside the compromised system

### Why does ransomware succeed even against well-protected organisations?
- It typically enters via phishing — bypasses technical defences entirely (Session 4 link)
- Once inside, it moves laterally before encrypting — by the time you notice, it's everywhere
- Nevada 2025: malware entered in May, ransomware triggered in June-July — **one month undetected**
- The lesson: detection speed matters as much as prevention — slow detection = larger blast radius

### Why is paying the ransom not a solution?
- Payment funds further attacks — you're financing criminal infrastructure
- No guarantee the attacker actually gives you the decryption key
- Even if they do, you still don't know how they got in — they might come back
- The real solution is: **working backups + fast detection + incident response plan**

### Why must backups be **immutable** and **offline** to protect against ransomware?
- Ransomware targets and encrypts everything it can reach — including network shares and connected backup drives
- If your backup is mounted or accessible from the infected system, it gets encrypted too
- **Immutable backups** cannot be changed once written — even by ransomware or a compromised admin account
- **Offline/air-gapped backups** are physically disconnected — unreachable by malware regardless of permissions

### Why is the 3-step model (Prevent → Detect → Recover) the right framework?
- Prevention alone fails — the Nevada and M&S cases prove that even large organisations get breached
- Without detection, an attacker lives undetected for weeks, maximising damage
- Without recovery capability, the only options are pay the ransom or rebuild from scratch
- A mature security posture addresses all three — not just the "prevent" layer

---

## Session 14 — Monitoring & Logging

### Why log everything, even when nothing is wrong?
- You don't know something is wrong until you check the logs
- Logs are your **time machine** — after an incident, logs tell you what happened, when, and how
- Nevada 2025: attackers had one month undetected because detection was slow — better logging = faster detection
- No logs = no forensics = no understanding = no improvement

### Why not save disk space by reducing logging?
- Disk is cheap; a breach is expensive
- The moment you need a log entry that doesn't exist, you realise disk was the wrong thing to save
- Logs are also required for compliance (GDPR, NIS2, ISO 27001 all require audit logs)
- Rule: **log everything, store for as long as required, protect the logs**

### Why log to a **remote** machine, not just locally?
- If the local system is compromised, the attacker can **delete or modify local logs**
- Remote logs on a separate, hardened machine cannot be tampered with from the compromised host
- This is called a **central log server** or **SIEM** (Security Information and Event Management)
- For forensics and compliance: logs must be tamper-evident — remote storage provides that

### Why not just read logs manually?
- A busy server generates thousands of log lines per day
- Manually reading logs = guaranteed to miss something important
- **Logcheck** solves this: it automatically filters normal noise and emails only anomalies
- The signal-to-noise problem is why automated log analysis tools exist — humans can't keep up

### Why use `lsof` for security monitoring?
- `lsof` shows every open file and network connection and the process holding it
- An attacker's backdoor will show up as a process with an unexpected open network connection
- Malware that reads sensitive files will appear as a process with those files open
- It's a snapshot of what the system is **actually doing** right now — hard to fake without a rootkit

### Why monitor system performance (Glances) as a security measure?
- Unexpected CPU or memory spikes can indicate a cryptominer, a brute force process, or active exploitation
- A server running at 100% CPU with no known workload is a red flag
- Performance monitoring is not just ops — it's one more signal in the detection layer
- Combined with logs: "CPU spike at 03:00 + failed SSH logins at 03:00" = probable attack

### Why is monitoring the final layer of defence, not an optional extra?
- Prevention (hardening, patching, firewall) reduces the chance of breach
- But no prevention is perfect — breaches happen to well-protected organisations
- Monitoring is what converts "we got breached" into "we detected it in 2 hours instead of 2 months"
- The faster the detection, the smaller the blast radius — monitoring is what enables fast detection

---

## Cross-Session Themes

### Why does the principle of least privilege appear everywhere?
- Sessions 2 (sudo), 5 (ACL), 6 (LDAP groups), 8 (AllowUsers), 11 (iptables), 13 (infection prevention)
- It's the single most effective way to **limit blast radius**
- When something goes wrong (and it will), least privilege determines how bad it gets
- A compromised account with minimal privileges = minimal damage

### Why does encryption appear everywhere?
- Sessions 2 (LUKS), 6 (LDAPS), 8 (SSH, key auth), 9 (SCP/SFTP)
- Data in transit and data at rest are both attack surfaces
- Encryption makes stolen data useless without the key
- Not just "nice to have" — required by GDPR, ISO 27001, NIS2

### Why do we always back up config files before editing?
- Sessions 8 (`sshd_config.bak`), 6 (slapd config), 11 (iptables rules)
- A config mistake can lock you out completely (SSH, sudo, LDAP, firewall)
- A backup means you can always restore the last known good state
- In production: always backup before changes — this is standard practice

### Why is "verify, never assume" a security principle?
- SSH root login: Ubuntu default is `prohibit-password` — but it must be **checked** on every system
- Assumption is the mother of all security failures
- Attackers rely on admins assuming things are configured correctly when they aren't

### Why does the "What, How, Why" model matter at the exam?
- Kristoffer says it explicitly: **the Why is important, the hows are just details**
- A student who can only describe *what* a tool does gets a low grade
- A student who explains *why* the tool exists, *what problem it solves*, and *how it fits into the bigger picture* gets the high grade
- Every topic in this document is an answer to a "why" — that's the level you're aiming for

### Why do the real-world incidents (M&S, Nevada) keep coming up?
- They prove that the theory has real consequences — this isn't abstract
- They show which defences failed and which would have helped
- Kristoffer uses them as exam discussion anchors — "what could have prevented this?"
- For each incident: be able to map it back to the sessions (Nevada = detection/logging, M&S = authentication)