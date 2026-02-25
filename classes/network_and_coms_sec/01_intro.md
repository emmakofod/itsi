# Network and Communication Security (NCS)
## 1. Course Overview

Not a pen testing class — focused specifically on **networks and network services**.

- Define what a hacker is (discuss!)
- Learn hacking techniques — network tools and attack vectors
- Learn what we can do to **prevent and limit** attacks

### The Security Framework (4 pillars)

```
         Prevent  ← main focus
            |
Respond — [Core] — Detect  ← secondary focus
            |
         Govern  ← least focus
```

> Priority: **Prevent > Detect > Respond/Govern**

---

## 2. Læringsmål (Learning Goals)

### Viden (Knowledge)
- Netværkstrusler (network threats)
- Trådløs sikkerhed (wireless security)
- Sikkerhed i TCP/IP
- Adressering i de forskellige lag
- Dybdegående kendskab til internet protokoller (SSL m.fl.)
- Hvilke enheder der anvender hvilke protokoller
- Sniffing strategier og teknikker
- Netværk management (overvågning/logning, SNMP)
- Forskellige VPN setups
- Gængse netværksenheder: firewall, IDS/IPS, honeypot, DPI

### Færdigheder (Skills)
- Overvåge netværk og netværkskomponenter (IDS/IPS, honeypot)
- Teste netværk for angreb mod de mest anvendte protokoller
- Identificere sårbarheder i et netværk

### Kompetencer (Competencies)
- Designe, konstruere, implementere og teste et sikkert netværk
- Monitorere og administrere et netværks komponenter
- Udfærdige en red team rapport om netværkssårbarheder
- Opsætte og konfigurere IDS/IPS
- Håndtere krypteringstiltag til sikring af netværkskommunikation

---

## 3. Course Topics

| Topic | In Course? |
|---|---|
| Security in TCP/IP | ✅ |
| Network attacks (scans, poisoning, spoofing, MITM, DDoS, brute force) | ✅ |
| Packet capture & Netflow | ✅ |
| Network segmentation / segmentering | ✅ |
| Firewalls & port security | ✅ |
| Network management & logs | ✅ |
| VPN (PPTP, IPSec, OpenVPN) | ✅ |
| Application layer attacks | ✅ |
| WiFi Security | ✅ |
| IDS/IPS | ✅ |
| SSH | ✅ |
| TLS and certificates | ✅ |
| Nmap / network scanning | ✅ |
| Spoofing, social engineering | ✅ |
| Malware, raspberry pies | ✅ |
| Packet analysis (all layers) | ⚠️ partial |
| Docker | ❌ not in this course |
| Burp Suite / DirBuster | ❌ not in this course |
| Privilege escalation | ❌ not in this course |

### Slide Color Key
Look for the small indicator box in the corner of each slide:

| Color | Meaning |
|---|---|
| 🟢 Green | Network Core |
| 🔵 Blue | DFIR (Digital Forensics & Incident Response) |
| 🔴 Red | Attacks |

---

## 4. Deliverables & Important Dates

### Deadlines
| Date | Deliverable | Where |
|---|---|---|
| 26/05/2026 | Both mandatory assignments | **Fronter** |
| 28/05/2026 | 1 A4 with bulletpoints on Mandatory 1 | **Wiseflow** |


### What to Hand In (6 things total)
1. **Mandatory 1** — Design a Network (1 exercise)
2. **Mandatory 2** — Solve 4 specific hands-on exercises (4 exercises)
3. **Wiseflow A4** — ~5–6 bullet points on Mandatory 1 covering interesting/discussable points for the exam

---

## 5. Exam

- **Format:** Individual, oral
- **When:** Approx. June, week 2
- **Process:**
  - A topic/question is drawn at random from **~7–8 topics**
  - You explain the topic → prepare slides/notes for **every topic**
  - Small discussion on **Mandatory 1**
- **Grading:** 7-point scale

### Important Exam Notes
- The oral discussion can include: *"what would you have done differently?"*
- Mandatory 1 is discussed at the exam; **Mandatory 2 is NOT part of grade**
- If you redesign your Mandatory 1 network based on what you learned in Mandatory 2 — that's fair game to discuss
