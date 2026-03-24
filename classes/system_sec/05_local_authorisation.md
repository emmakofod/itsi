# System Security — Session 5: Local Authorisation & ACL

---

## Protecting Data — The Two Steps

Before anything else, protecting data requires two things in order:

| Step | Question | Term |
|---|---|---|
| 1 | Who are you? | **Authentication** |
| 2 | What are you allowed to do? | **Authorisation** |

This session focuses on **local authorisation** — controlling who can do what on a single machine.

---

## Standard Unix Permissions (UGO) — And Why They're Not Enough

Unix file permissions use three categories:

| Category | Symbol | Meaning |
|---|---|---|
| User | `u` | The file owner |
| Group | `g` | Members of the file's assigned group |
| Others | `o` | Everyone else |

Each category gets three permission bits: **R**ead, **W**rite, e**X**ecute.

**The problem:** Real organisations have many overlapping groups — Sales-København, Sales-Jylland, Kontor, EconomicDept, Development, HelpDesk, Logistics... UGO can't represent this cleanly. You only get *one* group per file.

---

## Access Control Lists (ACL)

ACL is a more flexible system built on top of standard permissions. Each file/directory stores a **metadata header** containing a list of explicit rules — you can grant specific permissions to *any number* of users and groups.

**Key principle:** ACL lets you say things like:
- `group1` → read + write
- `group2` → read only
- `lotte` (individual user) → read + write
- everyone else → nothing

---

## ACL Commands

### Check if ACL is enabled
```bash
getfacl testfile.txt
```

### View ACL on a file/directory
```bash
getfacl accounts
```

### Set ACL permissions
```bash
# Syntax: setfacl -m <type>:<name>:<permissions> <target>

setfacl -m g:group1:rwx accounts      # group1 gets rwx
setfacl -m g:group2:r-x accounts      # group2 gets r-x only
setfacl -m other:--- accounts          # everyone else: no access
setfacl -m u:lotte:rwx accounts        # specific user lotte gets rwx
```

### Set permissions recursively (all files inside a directory)
```bash
setfacl -R -m u::rwx,g::---,o::--- /dir17
```

### Set **default** ACL (applies to new files created inside the directory)
```bash
setfacl -dR -m u::rwx,g::---,o::--- /dir17
setfacl -dR -m g:humhum:r-x /dir17
```
> Without `-d`, new files created inside the directory don't inherit the ACL — you need defaults for ongoing protection.

### Backup and restore ACL
```bash
# Backup
getfacl -R testdir > testdir_permissions.acl

# Restore
setfacl --restore=permissions.acl
```
> Always back up before changing permissions on important directories.

---

## Full Setup Walkthrough

```bash
# 1. Create users
sudo adduser user1
sudo adduser user2
sudo adduser user3

# 2. Create a group and add users
sudo addgroup group1
usermod -G group1 user1
usermod -G group1 user2
usermod -G group1 user3

# 3. Create a directory and set ownership
mkdir /testdir
chown user1 /testdir

# 4. As user1 — create a subdirectory
cd /testdir
mkdir accounts

# 5. Apply ACL
setfacl -m g:group1:rwx accounts
setfacl -m g:group2:r-x accounts
setfacl -m other:--- accounts

# 6. Verify
getfacl accounts
```

---

## Exercise 5.1 — Summary

The exercise builds a realistic company permission setup:

| Task | Command(s) |
|---|---|
| Create users peter, soren, gitte, lene, thomas, lotte, emil | `sudo adduser <name>` |
| Create group `salg` with peter, soren, gitte, lene | `sudo addgroup salg` + `usermod -G salg <name>` |
| Create group `kontor` with thomas, lotte, emil | `sudo addgroup kontor` + `usermod -G kontor <name>` |
| Create `/okonomi` in root, add txt files | `mkdir /okonomi` |
| Make `salgschef` the owner | `chown salgschef /okonomi` |
| `salg` → read + write, `kontor` → read only | `setfacl -m g:salg:rwx /okonomi` + `setfacl -m g:kontor:r-x /okonomi` |
| Give `lotte` write permission individually | `setfacl -m u:lotte:rwx /okonomi` |
| All others → no access | `setfacl -m other:--- /okonomi` |
| Apply defaults to match (for future files) | Repeat all with `setfacl -d ...` |

**What is this an example of?** → **Discretionary Access Control (DAC)** — the file owner controls who gets access.  
**What is it good for?** → Fine-grained, flexible permission management that matches real organisational structures, without needing UGO workarounds.

---

## Key Concepts for Exam

- **Authentication** answers "who are you?" — **Authorisation** answers "what can you do?" — always in that order
- **Standard Unix UGO** is too rigid for real organisations — only one group per file
- **ACL** stores a permission list in the file's metadata — supports any number of users and groups per file
- **`setfacl`** sets permissions, **`getfacl`** reads them
- **`-R`** flag = recursive (affects existing files/dirs inside), **`-d`** flag = default (affects *future* files)
- **Always back up ACL before modifying** with `getfacl -R > backup.acl`
- **Without default ACL**, new files created inside a directory won't inherit the rules