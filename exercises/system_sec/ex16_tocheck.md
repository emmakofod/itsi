# System Security — Session 16 Exercises
## Server Hardening Lists

**Goal:** Evaluate existing hardening lists, compare with AI-generated ones, and reflect on how a real company should build and maintain its own list.


# Exercise 16.1a — Evaluate a Hardening List (First 5 + 2 deep dives)

**Step 1 — Pick one list.** Pluralsight
> https://www.pluralsight.com/resources/blog/tech-operations/linux-hardening-secure-server-checklist

1. "Keep software updated" Makes sense, unpatched = known CVEs exploitable (Session 4)
2. "Disable root SSH login" Yes, done in Session 8, PermitRootLogin no 
3. "Use a firewall" Yes, iptables from Session 11 
4. "Remove unnecessary services" Session 3, every open port = attack surface
5. "Use strong passwords + 2FA" Session 7, PAM + Google Authenticator


## Deep dive on 2 points

**Point 1: "Disable unused services"**
- Every service running on a server is software, and software has bugs. An unused service that nobody monitors still has its port open and can be exploited.

- We verified this with nmap in Session 3. Scanning Metasploitable2 showed dozens of services running that nobody needs.

- Good advice because it directly reduces the attack surface. The only cost is the time to identify and stop the services, which is low compared to the risk.

**Point 2: "BIOS protection"**

- The BIOS controls the machine before the OS even starts, including what device to boot from. If an attacker can access the BIOS, they can set the machine to boot from a USB stick and bypass every OS-level control you've set up: disk encryption passphrase aside, all your file permissions, sudo rules, and SSH hardening become irrelevant.

- This is exactly the physical access attack discussed in Session 2 with LUKS. The advice here extends that thinking one layer deeper: even if the disk is encrypted, you want to prevent someone from easily loading a different OS to begin with.

- Good advice, but: it's primarily relevant when an attacker has physical access to the machine.
On a cloud server or a locked data centre rack, the risk is lower. The effort is low (set a BIOS password once), so there's no reason not to do it, but it's not a substitute for disk encryption.

Both together is the right answer.



# Exercise 16.1b — The Hardening List Sources

**Netwrix**  https://netwrix.com/en/resources/guides/linux-hardening-security-best-practices/

**Sternum**  https://sternumiot.com/iot-blog/linux-security-hardening-19-best-practices-with-linux-commands/

**Pluralsight** https://www.pluralsight.com/resources/blog/tech-operations/linux-hardening-secure-server-checklist

**Webasha** https://www.webasha.com/blog/what-are-the-most-important-linux-server-hardening-steps-to-secure-systems


# Exercise 16.2 — AI-Generated Hardening ListPrompt used:

"Give me a Linux server hardening checklist with at least 10 points. For each point include a brief explanation of why it matters."

AI-generated list (Claude, May 2026):
1. Keep the system updated (apt update && apt upgrade)
2. Disable root login over SSH (PermitRootLogin no)
3. Configure a host firewall (iptables / ufw)
4. Remove unnecessary packages and services
5. Enforce strong passwords and account lockout (PAM)
6. Use SSH key authentication and disable password login
7. Set correct file permissions on sensitive files (/etc/shadow, /etc/sudoers)
8. Enable and configure logging (rsyslog, send to remote server)
9. Set up fail2ban to block brute force attempts
10. Audit SUID/SGID files regularly
11. Configure automatic security updates (unattended-upgrades)
12. Disable unused network protocols (IPv6 if not needed, ICMP redirects)


## Evaluate points 1, 2, 3, and 7

**Point 1 "Keep the system updated" (apt update && apt upgrade)**
Good advice, patching is the #1 technical defence (Session 4).

Most exploits target known, already-documented CVEs. An unpatched system is an open invitation to anyone running Metasploit. Practical: one command, low effort. The only risk is that an update occasionally breaks something, which is why you test on staging first. Every hardening list includes this because it directly addresses the second most common attack vector.

**Point 2 "Disable root login over SSH" (PermitRootLogin no)**
Good advice: covered directly in Session 8. If root login is allowed and an attacker brute-forces SSH, they immediately have full system access with no further steps needed. Disabling it forces them to compromise a normal account first, then escalate — adding a step and more time for detection. Practical — one line in /etc/ssh/sshd_config, low effort. We did this ourselves and verified it works. The advice is correct, specific, and verifiable.

**Point 3 "Configure a host firewall (iptables / ufw)"**
Good advice: covered in Session 11. Without a firewall, every port on the server is reachable by default. iptables lets you define exactly which traffic is allowed and from where, and sets a default-deny policy so unknown traffic is blocked automatically. Practical with iptables — medium effort to set up rules properly and make them persist across reboots (iptables-save). The AI listing both iptables and ufw is slightly vague — ufw is a simpler frontend but generates the same iptables rules underneath. Still correct.

**Point 7 "Set correct file permissions on sensitive files"**
Good advice: directly covered in Sessions 2.5 and 5. Files like /etc/shadow (hashed passwords), /etc/sudoers (who can become root), and SSH config files must only be readable/writable by root. If any user can read /etc/shadow, they get all the password hashes and can crack them offline. If any user can write to /etc/sudoers, they can give themselves root. Practical — low effort, a few chmod and chown commands. The advice is correct but slightly vague — a better list would specify exactly which files and what permissions. Worth verifying each file's current permissions with ls -la before and after.


## Is the AI list better than the expert lists?

- **AI lists:** Comprehensive, structured, includes explanations, adapts to your specific question, up-to-date knowledge, explains the WHY
**BUT:**
Can hallucinate commands or answers, may give generic advice not suited to your specific OS version, no accountability for errors, can't know your specific environment
- **Expert lists:** Written by practitioners with real experience
**but:**
Vary in quality, can be outdated, sometimes no explanation ("just do this")

=> Neither is good enough alone. You can use both as input, then verify each point yourself against your actual environment. YOU need to take accountability and customize it to your needs.



# Exercise 16.3 — Company Hardening List Discussion

**Should your company have a server hardening list? Why?**
Yes: without a list, hardening depends on whoever sets up the server remembering everything.
People make mistakes! A checklist ensures consistency across all servers and across all engineers.
Also satisfies compliance reqs (ISO 27001, NIS2).



**What is similar across the lists you've seen?**
Almost every list includes: update software, disable root SSH, use a firewall, remove unnecessary services, use strong authentication. 

These are the universal baseline, they appear because they address the most common attack vectors.



**Why are there differences between lists?**
Different authors, different audiences (IoT vs web server vs enterprise), different OS versions, different threat models.
A list for a startup web server is different from one for a hospital's database server.

There is no 1 correct answer.



**Can you use an external list directly for your company? Can you use an AI list directly?**
No!! not directly. Every point needs to be:
1. Verified (Does it apply to us?)
2. Tested (does applying it break anything in our environment?)
3. Adapted (does our software require something that this point would block?)

An AI or expert list is a starting point, not a finished product.



**How should you select content for your company list?**
Start with a baseline (one reputable list), cross ref with others, remove points that don't apply to your environment, add company-specific requirements, test each point on a staging server before production, document the **WHY** for each point so future engineers understand the reasoning.



**Should all your servers have the same hardening list?**
No, a web server, a database server, and a mail server have different attack surfaces and different required services.
The baseline is the same, but server-role-specific rules will differ. ex: a web server needs port 443 open; a database server should have no public ports at all.



**How should you maintain the list?**
Review it regularly, at minimum annually, and also when:
- A major vulnerability is discovered
- You deploy a new type of server
- Software or OS versions change
- After a security incident

Treat it like code, version control it, review changes, document who changed what and why.



**What can you learn from this exercise?**
That security is not a product you buy: it's a process you maintain.
No list is complete or permanent. The value is in understanding the WHY behind each point, so you can adapt when something changes.



**Will AI replace you when you have work experience?**

> AI can generate lists and explain concepts
But AI cannot know your specific environment, test whether a hardening step breaks your application, take responsibility for a security incident, or make judgment calls under pressure.
A security professional with real experience, who understands the WHY, not just the HOW, is not replaceable by AI.
You become harder to replace the more you understand the reasoning behind the tools.
