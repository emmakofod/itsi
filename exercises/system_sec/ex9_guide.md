# Exercise 9.3 — Kerberos Configuration Guide

**Realm:** `EKKO.LOCAL`  
**Three machines:** KDC · SSH Server · SSH Client (Desktop)

---

## Step 0 — VM Setup

Clone your existing Ubuntu Server VM **twice** in VMware:

1. Right-click VM → **Clone** → Linked Clone (faster)
2. Name them clearly: `kdc-vm` and `ssh-server-vm`
3. Boot each one and set a unique hostname:

**On KDC VM:**
```bash
sudo hostnamectl set-hostname kdc.ekko.local
```

**On SSH Server VM:**
```bash
sudo hostnamectl set-hostname sshserver.ekko.local
```

Then note the IP of each VM:
```bash
ip a
```

Write them down — you'll need them soon. For this guide:
- `KDC_IP` = your KDC VM's IP
- `SSH_SERVER_IP` = your SSH Server VM's IP

---

## Step 1 — Edit /etc/hosts on ALL THREE machines

Every machine needs to know the others by hostname.  
Do this on **KDC, SSH Server, and Desktop**:

```bash
sudo nano /etc/hosts
```

Add these lines (swap in your real IPs):
```
KDC_IP          kdc.ekko.local          kdc
SSH_SERVER_IP   sshserver.ekko.local    sshserver
DESKTOP_IP      client.ekko.local       client
```

---

## Step 2 — Set Up the KDC

### 2.1 Install packages
```bash
sudo apt update
sudo apt install -y krb5-kdc krb5-admin-server
```

During install it asks three questions:
- **Default Kerberos realm:** `EKKO.LOCAL`
- **Kerberos servers:** `kdc.ekko.local`
- **Administrative server:** `kdc.ekko.local`

### 2.2 Create the realm database
```bash
sudo krb5_newrealm
```
It will ask for a master password — remember it, but it's just for this lab.

### 2.3 Create principals (accounts in Kerberos)

Open the admin tool:
```bash
sudo kadmin.local
```

Inside kadmin, run these commands one by one:

```
# Admin principal (for managing the KDC)
addprinc root/admin

# User principal (the person logging in — use your Linux username)
addprinc ekko

# Service principal for the SSH server
addprinc -randkey host/sshserver.ekko.local

# Export SSH server key to a keytab file
ktadd -k /tmp/sshserver.keytab host/sshserver.ekko.local

# Exit kadmin
quit
```

### 2.4 Copy the keytab to SSH Server

```bash
scp /tmp/sshserver.keytab ekko@SSH_SERVER_IP:/tmp/
```

### 2.5 Edit /etc/krb5kdc/kadm5.acl

Give the admin principal full rights:
```bash
sudo nano /etc/krb5kdc/kadm5.acl
```

Make sure this line exists (uncomment if needed):
```
*/admin *
```

### 2.6 Restart KDC services
```bash
sudo systemctl restart krb5-kdc
sudo systemctl restart krb5-admin-server
```

---

## Step 3 — Configure the SSH Server VM

### 3.1 Install Kerberos client tools
```bash
sudo apt update
sudo apt install -y krb5-user
```

Use the same answers as before:
- Realm: `EKKO.LOCAL`
- KDC: `kdc.ekko.local`
- Admin server: `kdc.ekko.local`

### 3.2 Place the keytab
```bash
sudo mv /tmp/sshserver.keytab /etc/krb5.keytab
sudo chmod 600 /etc/krb5.keytab
```

### 3.3 Edit SSH server config
```bash
sudo nano /etc/ssh/sshd_config
```

Find and set these values:
```
GSSAPIAuthentication yes
GSSAPICleanupCredentials yes
```

Make sure these are NOT blocking it:
```
KerberosAuthentication yes
UsePAM yes
```

### 3.4 Restart SSH
```bash
sudo systemctl restart ssh
sudo systemctl daemon-reload
```

---

## Step 4 — Configure the SSH Client (Ubuntu Desktop)

### 4.1 Install Kerberos client tools
```bash
sudo apt update
sudo apt install -y krb5-user
```

Same answers:
- Realm: `EKKO.LOCAL`
- KDC: `kdc.ekko.local`
- Admin server: `kdc.ekko.local`

### 4.2 Check /etc/krb5.conf looks right
```bash
cat /etc/krb5.conf
```

It should contain:
```ini
[libdefaults]
    default_realm = EKKO.LOCAL

[realms]
    EKKO.LOCAL = {
        kdc = kdc.ekko.local
        admin_server = kdc.ekko.local
    }

[domain_realm]
    .ekko.local = EKKO.LOCAL
    ekko.local = EKKO.LOCAL
```

If it looks wrong, edit it:
```bash
sudo nano /etc/krb5.conf
```

---

## Step 5 — Test & Demo

### 5.1 Get a Kerberos ticket (on the Desktop/Client)
```bash
kinit ekko
```
Enter the password you set for the `ekko` principal in Step 2.3.

### 5.2 Verify you have a ticket
```bash
klist
```
You should see something like:
```
Credentials cache: ...
        Principal: ekko@EKKO.LOCAL

  Issued              Expires             Principal
  May 03 ...          May 04 ...          krbtgt/EKKO.LOCAL@EKKO.LOCAL
```

### 5.3 SSH into the server using Kerberos
```bash
ssh -v -o GSSAPIAuthentication=yes ekko@sshserver.ekko.local
```

The `-v` flag shows verbose output so you can see Kerberos auth happening.  
Look for a line like:
```
debug1: Authentication succeeded (gssapi-with-mic)
```

That's it — **Kerberos authentication is working!** 🎉

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `kinit: Cannot contact any KDC` | Check `/etc/hosts` on client, ping `kdc.ekko.local` |
| `ssh: GSSAPI error` | Check keytab is at `/etc/krb5.keytab` on SSH Server, check hostname matches principal |
| Clock skew error | Kerberos requires clocks within 5 min — run `sudo timedatectl` on all machines and sync time |
| `kadmin.local: Cannot open DB` | Run `sudo krb5_newrealm` again or check KDC service is running |

---

## Cleanup (after demo)

Destroy your ticket when done:
```bash
kdestroy
```