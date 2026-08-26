# System Security – Notes 9
## Secure File Transfer & Kerberos

---

## 1. Secure File Transfer — SCP & SFTP

Both use **SSH as the transport layer** → traffic is encrypted by default.  
FTP is **not encrypted** — never use it. Credentials and file contents are sent in plaintext.

---

### SCP (Secure Copy)

- Bare-bones file copy over SSH
- You must specify the **full path** of source and destination
- Faster than SFTP (fewer ACKs exchanged) — only relevant for very large files
- Cannot create directories or delete files on the remote

```bash
# Copy a file TO the server
scp -P 22123 bla.txt user1@192.168.x.x:/home/user1/

# Copy a directory TO the server (-r = recursive)
scp -r -P 22123 testdir1/ user1@192.168.x.x:/home/user1/

# Copy a file FROM the server
scp -P 22123 user1@192.168.x.x:/home/user1/bla2.txt ./bla2.txt
```

> Note: SCP uses capital `-P` for port (SSH uses lowercase `-p`)

---

### SFTP (Secure FTP)

- Also uses SSH for transport and encryption
- More feature-rich than SCP: can **create directories**, **delete files**, **browse** remote filesystem interactively
- Does **not** need you to specify full path upfront — you navigate like an FTP session
- Slightly slower than SCP due to more ACKs
- **Preferred for general use** — SCP only wins on raw speed for massive transfers

```bash
sftp -P 22123 user1@192.168.x.x
# Then interactive commands: ls, cd, get, put, mkdir, rm
```

---

### SCP vs SFTP Summary

| | SCP | SFTP |
|---|---|---|
| Encryption | ✅ SSH | ✅ SSH |
| Needs full path | ✅ Yes | ❌ No (interactive) |
| Create directories | ❌ No | ✅ Yes |
| Delete files | ❌ No | ✅ Yes |
| Speed | Faster | Slightly slower |
| Best for | Quick scripted transfers | General use |

---

## 2. Kerberos

### LDAP vs Kerberos — What's the difference?

LDAP gives you:
- Central user administration
- Central user authentication

But LDAP does **not** give you:
- **Single Sign-On (SSO)** — user still has to enter password for each new service
- **No password/hash sent over network** — LDAP sends credentials that can be intercepted

Kerberos adds both of those things on top.

---

### What is Kerberos?

- An **authentication protocol** designed for use over untrusted networks
- Uses **cryptography** to protect all data sent and to verify identity
- Uses a **trusted, dedicated third-party server** for authentication and authorisation
- One login = access to all resources for the duration of the ticket (typically one work day, ~10 hours — configurable)
- Passwords and hashes are **never sent over the network**
- Windows **Active Directory** is Microsoft's implementation of Kerberos
- Other commercial products also implement the Kerberos protocol

---

### Key Components

| Component | Role |
|---|---|
| **KDC** (Key Distribution Center) | The Kerberos server — contains AS + TGS |
| **AS** (Authentication Server) | Verifies user identity at login, issues TGT |
| **TGS** (Ticket Granting Server) | Issues service tickets based on valid TGT |
| **TGT** (Ticket Granting Ticket) | Proof that you've logged in — used to request service tickets |
| **Service Ticket** | Proof that you're allowed to access a specific service |
| **Principal** | Any entity in Kerberos — a user, a service, or a host |
| **Realm** | The Kerberos domain (e.g. `KERBEROS.KEA.DK`) |
| **Keytab** | A file containing a service's cryptographic key — used instead of a password |

---

### Kerberos Auth Flow (6 steps)

```
1) Client → AS:        "I want to log in" (username, no password sent)
2) AS → Client:        TGT encrypted with client's key (derived from password)
3) Client → TGS:       "I want access to service X" + TGT
4) TGS → Client:       Service Ticket for service X
5) Client → Server:    "Here's my service ticket"
6) Server → Client:    Access granted ✅
```

**Key insight:** The password is only used locally to decrypt the TGT (step 2). It never leaves the client machine.

---

### Infrastructure Requirements

- **Minimum 3 machines:**
  - Kerberos server (dedicated — fewer services = better protected)
  - SSH server (the service being protected)
  - SSH client (the user machine)
- All machines must be able to **ping each other**
- All machines must have **synchronised clocks** — Kerberos is time-sensitive, rejects tickets more than **5 minutes** out of sync
- A **secondary Kerberos server** is recommended in production for availability — if the KDC goes down, no one can log in anywhere

---

### Setup Overview (lab)

**On all machines** — edit `/etc/hosts` to know each other by hostname:
```
192.168.x.x  kerberos.kea.dk
192.168.x.x  sshserver.kea.dk
192.168.x.x  sshclient.kea.dk
```

**Kerberos server:**
```bash
sudo apt install krb5-admin-server krb5-kdc
sudo krb5_newrealm                        # create the realm
# Realm: KERBEROS.KEA.DK
```

Edit `/etc/krb5.conf` — add to `[domain_realm]`:
```
.kerberos.kea.dk = KERBEROS.KEA.DK
kerberos.kea.dk  = KERBEROS.KEA.DK
```

Add principals (users and services):
```bash
sudo kadmin.local
addprinc user11/admin      # user principal
addprinc root/admin        # root principal
addprinc -randkey host/sshserver.kea.dk   # SSH server principal
```

Create keytab for SSH server and copy it over:
```bash
ktadd -k /tmp/sshserver.kea.dk.keytab host/sshserver.kea.dk
sudo scp /tmp/sshserver.kea.dk.keytab user11@sshserver.kea.dk:/etc/krb5.keytab
```

**SSH server:**
```bash
sudo apt install krb5-config
# Edit /etc/ssh/sshd_config:
GSSAPIAuthentication yes
GSSAPICleanupCredentials yes
sudo service ssh restart
```

**SSH client:**
```bash
sudo apt install krb5-user
# Edit /etc/ssh/ssh_config:
GSSAPIAuthentication yes
GSSAPIDelegateCredentials yes

# Get a ticket:
kinit user11/admin
klist -A          # verify ticket is there

# Login — no password prompt!
ssh user11@sshserver.kea.dk
```

---

### Why Kerberos is better than plain LDAP for auth

| Feature | LDAP | Kerberos |
|---|---|---|
| Central user management | ✅ | ✅ |
| Central authentication | ✅ | ✅ |
| Single Sign-On (SSO) | ❌ | ✅ |
| Password sent over network | ⚠️ Yes (risk) | ❌ Never |
| Works over untrusted networks | ⚠️ Risky | ✅ Designed for it |
| Time-sensitive | ❌ | ✅ (5 min clock skew tolerance) |