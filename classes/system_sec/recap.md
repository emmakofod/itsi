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

## Cross-Session Themes

### Why does the principle of least privilege appear everywhere?
- Sessions 2 (sudo), 5 (ACL), 6 (LDAP groups), 8 (AllowUsers)
- It's the single most effective way to **limit blast radius**
- When something goes wrong (and it will), least privilege determines how bad it gets
- A compromised account with minimal privileges = minimal damage

### Why does encryption appear everywhere?
- Sessions 2 (LUKS), 6 (LDAPS), 8 (SSH, key auth)
- Data in transit and data at rest are both attack surfaces
- Encryption makes stolen data useless without the key
- Not just "nice to have" — required by GDPR, ISO 27001, NIS2

### Why do we always back up config files before editing?
- Sessions 8 (`sshd_config.bak`), 6 (slapd config)
- A config mistake can lock you out completely (SSH, sudo, LDAP)
- A backup means you can always restore the last known good state
- In production: always backup before changes — this is standard practice

### Why is "verify, never assume" a security principle?
- SSH root login: Ubuntu default is `prohibit-password` — but it must be **checked** on every system
- Assumption is the mother of all security failures
- Attackers rely on admins assuming things are configured correctly when they aren't