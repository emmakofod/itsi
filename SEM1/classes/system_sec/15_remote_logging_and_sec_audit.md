# Session 15 – Remote Logging & Security Auditing with Lynis

---

## 📌 Key Concepts

### Why log to a remote server?

When a server crashes or gets compromised, local logs may be:
- **Unreadable** (hardware failure, corrupted filesystem)
- **Tampered with** (attacker deletes/edits logs to hide their tracks)

By writing logs **simultaneously** to a remote log server:
- If the server crashes → read the log on the remote machine (like a black box in a plane)
- If the server is compromised → **compare** local vs. remote logs. Discrepancies = what the attacker tried to hide

---

## 🔧 Tool: rsyslog

- rsyslog = a syslog daemon that supports forwarding logs over the network
- Already installed on Ubuntu by default
- Supports both **UDP** and **TCP** transport
  - **TCP is preferred** → connection-oriented, guarantees delivery, harder to spoof
  - UDP is faster but unreliable — you might lose log entries
- Default port: **514**

### Setup overview

**On the remote log server** (`/etc/rsyslog.conf`):
- Uncomment the lines that enable UDP or TCP log reception:
  ```
  # For TCP:
  module(load="imtcp")
  input(type="imtcp" port="514")
  ```
- Restart: `sudo service rsyslog restart`

**On the local server** (the one sending logs):
- Create `/etc/rsyslog.d/10-rsyslog.conf`
- Add:
  ```
  *.* @remote.server.ip:514      # UDP (single @)
  *.* @@remote.server.ip:514     # TCP (double @@)
  ```
- Restart rsyslog: `sudo service rsyslog restart`

> **Tip:** `@@` = TCP, `@` = UDP — double = reliable

---

## 🔍 Tool: Lynis

- Lynis is a **security auditing tool** for Linux systems
- It scans the system and produces a report with:
  - **Warnings** → active issues that should be fixed
  - **Suggestions** → improvements to harden the system
- Log file: `/var/log/lynis.log`

### Useful commands
```bash
sudo lynis audit system               # Full audit
grep "Warning" /var/log/lynis.log     # Filter warnings
grep "Suggestion" /var/log/lynis.log  # Filter suggestions
```

### What does Lynis check?
- Installed packages and outdated software
- Open ports and running services
- File permissions
- SSH configuration
- PAM / password policies
- Kernel hardening settings
- And much more...

---

## 💡 "What is more secure?" — The answer

A server is most secure when it has:
1. **Only the services it needs** (minimal attack surface)
2. **All software updated** (patches close known vulnerabilities)
3. **No default/unnecessary services running**

The combination of all three = defense in depth.

---

---

