# System Security — Session 16 Notes
## Server Hardening Lists

---

## Why This Session Exists

Every other session taught you a specific tool or technique:
- Session 3 → scan with Nmap
- Session 8 → harden SSH
- Session 11 → configure iptables
- Session 14 → set up logging

**This session asks: how do you remember to do ALL of it — consistently, every time, on every server?**

The answer is a **hardening checklist**.

---

## Why We Make Lists

Kristoffer's analogy: a pilot's pre-flight checklist.

- A pilot with 20 years of experience still uses a checklist before every flight
- Not because they forgot — because **one missed step can be catastrophic**
- Security hardening is the same: 20–40 things to configure, and humans make mistakes under pressure

A checklist:
- Ensures **consistency** — every server gets the same baseline regardless of who set it up
- Provides **accountability** — you can show auditors what was done and when
- Satisfies **compliance** — ISO 27001, NIS2, and similar frameworks require documented, repeatable procedures
- Captures **institutional knowledge** — when an admin leaves, the list stays

---

## The Problem With External Lists

There are hundreds of Linux hardening lists on the internet. The problem:

| Issue | Why it matters |
|-------|---------------|
| Unknown author | "Expert" is a label anyone can claim |
| No explanation | "Do this" without WHY = you can't adapt it |
| Wrong OS version | Ubuntu 18.04 advice may be irrelevant or harmful on 24.04 |
| Wrong environment | A list for web servers ≠ a list for database servers |
| Outdated | A 2019 list doesn't know about 2023 vulnerabilities |
| Length varies wildly | 5 steps, 15 steps, 40 steps — none is automatically better |

**Rule: never copy-paste a hardening list. Verify every point.**

---

## What Good Hardening Lists Have in Common

Despite their differences, almost every reputable list includes these:

| Point | Session it connects to |
|-------|----------------------|
| Keep software updated | S3/S4 — patching kills known CVEs |
| Disable root SSH login | S8 — PermitRootLogin no |
| Configure a firewall | S11 — iptables |
| Remove/disable unnecessary services | S3 — every open port = attack surface |
| Use strong authentication + 2FA | S7 — PAM, Google Authenticator |
| Use SSH key authentication | S8 — disable password auth |
| Configure logging | S14/S15 — local + remote |
| Set correct file permissions | S2.5/S5 — chmod, ACL |
| Use least privilege (no shared root) | S2 — sudo, RBAC |
| Monitor for suspicious activity | S12/S14 — Tripwire, logcheck |

These are the **universal baseline** — they address the most common attack vectors.

---

## Why Lists Differ

Different lists have different lengths and content because:

- **Different threat models** — a public e-commerce server vs an internal HR server face different attacks
- **Different server roles** — web server, database, mail server, file server all have different required services
- **Different audiences** — beginner quick-start vs enterprise compliance standard
- **Different OS versions** — steps change between Ubuntu releases
- **Different dates** — security landscape evolves, older lists miss newer threats

**Longer is not automatically better.** A 40-point list with no explanations is less useful than a 15-point list where you understand every item.

---

## AI-Generated Hardening Lists

### Strengths
- Comprehensive — covers many domains at once
- Often includes explanations (better than many "expert" lists)
- Adapts to your specific question
- Fast to generate
- Generally reflects broad consensus from its training data

### Weaknesses
- Can **hallucinate** — invent commands, wrong syntax, wrong OS
- Generic — doesn't know your specific environment or software stack
- No accountability — if it's wrong, nobody answers for it
- Can give contradictory advice across different questions
- Cannot test whether its advice actually works in your setup

### The check for an AI list is identical to an expert list
> Verify each point independently. Test it. Understand the WHY. Don't apply it blindly.

---

## Building a Company Hardening List

### Step 1 — Start with a reputable baseline
Pick one well-known list (Pluralsight, Netwrix, CIS Benchmarks) as your foundation.

### Step 2 — Cross-reference
Compare 2–3 lists. Points that appear in all of them are almost certainly valid baseline items.

### Step 3 — Verify each point
For each item: does this command work on our OS version? Does it break anything in our stack?

### Step 4 — Test on staging
Never apply untested hardening to production. Test on a clone first.

### Step 5 — Adapt to your environment
- Add company-specific requirements
- Remove points that don't apply to your server roles
- Add the WHY for each point so future admins understand

### Step 6 — Maintain it
Review at minimum:
- Annually
- After a major vulnerability is discovered
- When OS or software versions change
- After a security incident

---

## Should All Servers Have the Same List?

**No.** Servers have different roles and therefore different requirements.

| Server type | What's different |
|-------------|-----------------|
| Web server | Needs port 80/443 open, web server process hardening |
| Database server | No public ports, strict network access rules |
| Mail server | SMTP/IMAP ports, relay configuration |
| File server | SMB/NFS hardening, share permissions |

**What IS shared:** the baseline — update software, firewall, strong auth, minimal services, logging.
**What DIFFERS:** role-specific service configuration.

---

## The "Will AI Replace You?" Question

Kristoffer asks this directly in Exercise 16.3. Here's the answer:

AI can:
- Generate a hardening list in seconds
- Explain what a command does
- Summarise documentation

AI cannot:
- Know your specific environment
- Test whether hardening step X breaks your application
- Make judgment calls during a live incident
- Take responsibility when something goes wrong
- Understand the business context behind a security decision

**The more you understand the WHY behind every tool and decision, the less replaceable you are.**

A security professional who can say *"I chose this approach because our threat model prioritises X, and this control addresses Y while avoiding the Z trade-off"* is not replaceable by a prompt.

---

## Useful Links (from Kristoffer's slides)

| Source | URL |
|--------|-----|
| Netwrix (2025) | https://netwrix.com/en/resources/guides/linux-hardening-security-best-practices/ |
| Sternum — 19 practices (2024) | https://sternumiot.com/iot-blog/linux-security-hardening-19-best-practices-with-linux-commands/ |
| Pluralsight — 15 steps (2022) | https://www.pluralsight.com/resources/blog/tech-operations/linux-hardening-secure-server-checklist |
| Webasha (2025) | https://www.webasha.com/blog/what-are-the-most-important-linux-server-hardening-steps-to-secure-systems |

---

## Key Concepts for Exam

- **Why hardening lists exist** — humans forget, checklists enforce consistency, compliance requires documentation
- **Why you can't copy-paste external lists** — wrong OS version, wrong environment, no explanation = can't adapt
- **What all lists agree on** — update, firewall, disable root SSH, remove unused services, strong auth, logging
- **Why lists differ** — different threat models, server roles, audiences, OS versions
- **AI lists** — good starting point, same verification rules as expert lists, cannot replace judgment
- **Company list** — verified, tested, adapted, maintained, documented with WHY for each point
- **Not all servers the same** — shared baseline, role-specific layer differs
- **The big picture** — a hardening list is a summary of everything in this course. Session 16 is the course wrapping up on itself.