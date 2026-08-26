# Notes 6 — Central Control, Authentication & LDAP

---

## Why Central Control?

- Companies have many servers and laptops
- Without central control: inconsistent user management across machines
- Central control gives:
  - **Visibility** — you can see all users and permissions in one place
  - **Manageability** — changes apply everywhere at once
  - **Consistency** — no random/conflicting configurations

### Key concepts

- **Authentication** — *Who are you?* Verifying identity (e.g. username + password)
- **Authorisation** — *What are you allowed to do?* Permissions after identity is confirmed

---

## What is LDAP?

**Lightweight Directory Access Protocol**

- A protocol for querying and modifying a directory service
- Based on the X.500 standard, runs over TCP/IP
- A **directory** = a hierarchical tree of entries (like a phone book for users/resources)
- Microsoft Active Directory (AD) is one implementation of LDAP

### Structure

- The directory is a **tree** (hierarchical)
- Each entry has a unique **DN (Distinguished Name)**
- Each entry has **attributes** (name, email, phone, group membership, etc.)

---

## LDAP Attributes (Common)

| Short | Full name |
|-------|-----------|
| CN | commonName |
| OU | organizationalUnitName |
| DC | domainComponent |
| O | organizationName |
| UID | userid |
| L | localityName |
| C | countryName |

---

## LDAP DN Examples

DNs are **read right to left** (most general → most specific):

```
OU=Distribution Groups,DC=gp,DC=gl,DC=google,DC=com
UID=Bob Smith,OU=People,DC=gp,DC=gl,DC=google,DC=com
CN=Dev-Idia,OU=Distribution Groups,DC=gp,DC=gl,DC=google,DC=com
```

### Example entry with 11 attributes:

```
dn: cn=John Jensen,ou=people,dc=eksempel,dc=ek,dc=dk
cn: John Jensen
givenName: John
sn: Jensen
telephoneNumber: +45 46 46 11 28
mail: john.jensen@eksempel.dk
manager: cn=Peter Jones,ou=people,dc=eksempel,dc=dk
objectClass: inetOrgPerson
```

---

## Why LDAP? (The Purpose)

- Many servers and user PCs → don't want to configure the same accounts everywhere
- Central LDAP server holds **one set of users** for all machines
- Any machine can ask the LDAP server for user authentication
- A user can log in on **any machine** as long as it can reach the LDAP server
- Easier maintenance — change a password once, applies everywhere

---

## LDAP Server Installation (Ubuntu)

```bash
# Set hostname
sudo hostnamectl set-hostname ldap.eksempel.dk
# Add to /etc/hosts:
# 192.168.x.x ldap.eksempel.dk

# Install
sudo apt-get update
sudo apt-get install slapd ldap-utils

# Reconfigure
sudo dpkg-reconfigure slapd
# Questions:
# Omit config? → No
# DNS domain name → eksempel.dk
# Organisation name → eksempel
# Admin password → (write it down!)
# Remove DB when purged? → No
# Move old DB? → Yes

# Verify
sudo slapcat
```

---

## LDAP Account Manager (LAM)

Web interface for managing LDAP — easier than command line for learning.

```bash
# Install Apache + PHP first, then LAM
# Default login: lam / lam
# Login as admin to create groups and users
```

### Important: UID/GID numbers

- Local Linux users are in the **1000–1999** range
- LDAP users must use **high numbers** to avoid collisions:
  - Groups: start at **5000**
  - Users: start at **10000**

---

## LDAP Client Installation (Ubuntu)

```bash
# Add LDAP server to /etc/hosts first

sudo apt-get update
sudo apt -y install libnss-ldapd libpam-ldap ldap-utils

# Restart service
sudo systemctl restart nscd

# Test
getent passwd         # should show LDAP users
cat /etc/passwd       # will NOT show LDAP users — compare the difference!

# Switch to LDAP user (without them being in /etc/passwd)
su jdoe
```

---

## LDAP Additional Tasks (Good to Know for Exam)

| Task | Why |
|------|-----|
| **Logging** | Track every query and login to LDAP |
| **Replication** | Backup LDAP server — if primary fails, clients still work |
| **ACL** | LDAP can also control resource permissions, not just auth |
| **TLS encryption** | Encrypts LDAP traffic — without it, credentials sent in plaintext |
| **Backup** | Plan for restoring the directory if it's lost |

---

## Recap — Key Questions

**What is LDAP an example of?**
Centralised identity and access management (IAM). A directory service that handles both authentication (who you are) and can support authorisation (what you can do).

**Why do we want this?**
- Single point of management for all users
- Consistent permissions across all machines
- Easier to onboard/offboard users
- Audit trail of who has access to what
- Without it: every machine has its own user list → chaos, inconsistency, security risk
