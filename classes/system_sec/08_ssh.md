# System Security – Notes 8
## Remote Authentication & SSH

---

## Remote Login Overview

Remote login = users authenticating to a **central service over the network** (mail, HR, CRM, billing, SSH...)

- Old protocols `rlogin` and `rsh` are **unencrypted** — remove them
- Use **OpenSSH** instead — encrypts all traffic between client and server
- SSH is used as a lab demo service (it's just the example — imagine it's your billing system)

```bash
sudo apt install openssh-server
sudo service ssh start
service --status-all | grep ssh    # check if running
```

---

## Hardening SSH — sshd_config

Always back up before editing:
```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sudo nano /etc/ssh/sshd_config
```

After any change:
```bash
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket
```

---

### 1. Change Default Port

```
Port 22123
```

- Automated bots constantly scan port 22
- Moving to a non-standard port drops off most automated attack traffic
- Security through obscurity — not a real defence alone, but reduces noise and log spam
- Test: `nmap` scans port 22 by default → SSH won't show up

---

### 2. Disable Root Login

```
PermitRootLogin no
```

- Ubuntu default is `prohibit-password` (commented out) — always verify, never assume
- With root disabled: attacker must compromise a normal user first, then escalate
- Adds an extra step to the attack chain — more time for detection

---

### 3. Restrict Users / Groups

```
AllowUsers user1 user2
AllowGroups sshusers
```

- Least privilege: only people who actually need SSH access should have it
- Fewer accounts = fewer brute force targets
- If credentials are stolen, they can't SSH in if not in the allow list

---

### SSH Hardening Summary

| Protection | Config line | Why |
|---|---|---|
| Non-standard port | `Port 22123` | Avoids automated scanning |
| Disable root login | `PermitRootLogin no` | Prevents direct root access |
| Restrict users | `AllowUsers` / `AllowGroups` | Least privilege |
| Encrypted traffic | Default in SSH | Prevents eavesdropping |
| Session timeout | `ClientAliveInterval` | Closes idle sessions |
| Geographic restriction | Firewall / fail2ban | Limits attack surface |

---

## Public/Private Key Authentication

Password = something you **know** → guessable, phishable, reusable  
Private key = something you **have** → 256-bit, ~10⁷⁵ combinations, not guessable

---

### Key Generation (on client, as the user)

```bash
su - user2
ssh-keygen -t rsa
# Keys saved to ~/.ssh/
# id_rsa     → private key (NEVER share)
# id_rsa.pub → public key (safe to copy)
```

Add a **passphrase** when prompted — protects the key file if stolen.

---

### Copy Public Key to Server

```bash
ssh-copy-id -p 22123 user2@172.16.121.131
# Adds public key to ~/.ssh/authorized_keys on the server
```

---

### Disable Password Login (force key-only)

In `/etc/ssh/sshd_config` on the server:
```
PasswordAuthentication no
```

Restart after:
```bash
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket
```

Now only users with a valid key can log in — no password = no brute force possible.

---

### Why the Public Key is Safe to Copy/Sniff

Asymmetric cryptography: what one key encrypts, only the other can decrypt.  
The public key can only **verify** — it cannot be used to log in.  
An attacker with the public key still needs the private key to authenticate.

---

### Key Auth + Passphrase = True 2FA

| Factor | Element |
|---|---|
| Something you **have** | The private key file |
| Something you **know** | The passphrase |

→ Key alone = 1 factor. Key + passphrase = **true 2FA**.

---

## sudo and su After Remote Login

- Root login disabled → attacker must compromise a normal user first
- Even then, `sudo` only works for users listed in `/etc/sudoers`
- To restrict the `su` command itself → change permissions/ACL on `/bin/su`

---

## Lab Config (our setup)

| Setting | Value |
|---|---|
| Server IP | `172.16.121.131` |
| SSH port | `22123` |
| Root login | Disabled (`no`) |
| Allowed group | `sshusers` (user1, user2) |
| Key auth | user2 has RSA key |
| Password auth | Disabled |