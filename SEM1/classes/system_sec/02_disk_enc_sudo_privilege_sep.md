# System Security — Sessions 2 & 2.5

---

## Session 2: Disk Encryption, Sudo & Privilege Separation

---

### Why Protect Parked Data?

- Data at rest lives on a hard drive, protected by OS access controls
- **Problem:** an attacker with physical access can boot their own OS from USB and bypass all OS controls — the attacker's OS owns the disk
- **Solution:** disk encryption

---

### Disk Encryption (LUKS)

**What it does:** encrypts the disk so data is unreadable without the key, even if the disk is copied or the machine is booted from USB.

**LUKS** = Linux Unified Key Setup — standard disk encryption on Linux

**How to set it up (Ubuntu):**
```
Installation type → Erase disk and install → Advanced features
→ Select LVM + "Encrypt the new Ubuntu installation"
```

**VMware alternative:** encrypt the virtual machine file from VMware settings after installation.

**Key points:**
- If you lose the key → data is unrecoverable
- Keep the key documented in a safe, known location
- All company disks (servers + laptops) should be encrypted
- Must be described in IT policy and procedures
- Windows: BitLocker (availability depends on version/edition)

**How to verify encryption is working:**
- From the host OS, open the VM's `.vmdk` file in a hex editor
- Unencrypted VM → readable file/directory names visible
- Encrypted VM → only random-looking binary data visible

---

### Root / Admin Users

- Root can do **anything** — no restrictions
- **Problems with sharing root:**
  - No accountability (who did what?)
  - One mistake = full system impact
  - Credential sharing is a security risk

---

### Sudo Access

**Concept:** give individual admin users `sudo` to run privileged commands — instead of sharing the root password.

```bash
adduser admin1          # create user
addgroup admin          # create group
usermod -aG admin admin1  # add user to group
visudo                  # edit /etc/sudoers safely (ALWAYS use visudo!)
```

**Why `visudo`?** It validates syntax before saving — a broken sudoers file can lock you out of your system entirely.

**Basic sudoers line format:**
```
user  host=(run_as_user:group)  command
```

**Examples:**
```
root   ALL=(ALL:ALL) ALL       # root can do everything
%admin ALL=(ALL)    ALL        # admin group can do everything
%sudo  ALL=(ALL:ALL) ALL
```

---

### Privilege Separation

**Core principle:** not every user/admin needs access to everything. Limit scope of damage if an account is compromised.

**Examples:**
- Economic dept, Sales dept, IT dept → different data access
- DB admin, Network admin, System admin → different system access

**`/etc/sudoers` aliases:**

| Alias type | Purpose | Example |
|---|---|---|
| `User_Alias` | Group users by name | `User_Alias OPERATORS = alice, bob` |
| `Host_Alias` | Restrict by IP/hostname | `Host_Alias OPNET = 192.168.1.0/24` |
| `Cmnd_Alias` | Group allowed commands | `Cmnd_Alias PRINTING = /usr/sbin/lpc` |
| `Runas_Alias` | Which users they can act as | `Runas_Alias OP = root, operator1` |

**Full example:**
```
User_Alias  OPERATORS  = kristoffer, peter
Host_Alias  OPNET      = 192.168.249.0/24
Cmnd_Alias  PRINTING   = /usr/sbin/lpc, /usr/bin/lprm
Cmnd_Alias  POWERCMD   = /bin/systemctl
Cmnd_Alias  NETCMD     = /sbin/ifconfig, /sbin/ip, /bin/ping

OPERATORS   ALL=ALL                    # full sudo for operators
user3       ALL=PRINTING               # only printer commands
user17      ALL=POWERCMD               # only power/service commands
user_net    OPNET=NETCMD              # network cmds from internal IPs only
wow         ALL=(ALL) NOPASSWD: ALL   # no password required (risky!)
```

**Protecting commands without sudo:**
- Some commands don't need sudo but should still be restricted
- Remove execute permission from `others`: `chmod o-x /sbin/shutdown`

---

### Exercises — Session 2

**2.1 — Disk encryption:**
- Create a new Linux VM with LUKS encryption enabled during install
- Verify: open the `.vmdk` in a hex editor from the host — encrypted = unreadable

**2.2a — Sudo admin user:**
```bash
adduser admin1
addgroup admin
usermod -aG admin admin1
visudo
# Add: %admin ALL=(ALL:ALL) ALL
```

**2.2b — Privilege separation:**
```bash
# Create users: netop1, netop2, printop1, printop2, powop1, powop2
# In visudo:
User_Alias NET_OP   = netop1, netop2
User_Alias PRINT_OP = printop1, printop2
User_Alias POW_OP   = powop1, powop2

Cmnd_Alias PRINTING = /usr/sbin/lpc, /usr/bin/lprm
Cmnd_Alias POWER    = /sbin/shutdown, /sbin/halt, /sbin/reboot
Cmnd_Alias NETWORK  = /sbin/route, /sbin/ifconfig, /sbin/ip, /bin/ping

PRINT_OP ALL=PRINTING
POW_OP   ALL=POWER
NET_OP   ALL=NETWORK
```

**2.2c — Windows equivalent:**
- Yes — same principle applies on Windows
- Use **Local Security Policy** or **Active Directory Group Policy**
- Assign roles via groups (Administrators, Backup Operators, etc.)
- Principle of Least Privilege — same concept, different tool

---

## Session 2.5: Linux Filesystem & File Management

---

### The Linux Filesystem Hierarchy

| Directory | Contents |
|---|---|
| `/` | Root — top of the entire filesystem |
| `/bin` | Essential binaries for all users (ls, cp, cat…) |
| `/sbin` | System binaries — admin/root tools (fsck, reboot…) |
| `/usr` | User programs and data (installed software) |
| `/usr/bin` | Non-essential user binaries (python, git…) |
| `/usr/sbin` | Non-essential system binaries (apache2, nginx…) |
| `/home` | User home directories (`/home/emma`) |
| `/etc` | System-wide config files (sudoers, hosts, passwd…) |
| `/dev` | Device files (disks, terminals, USB…) |
| `/tmp` | Temporary files — cleared on reboot |
| `/var` | Variable data: logs, mail, databases (`/var/log`) |
| `/lib` | Shared libraries needed by `/bin` and `/sbin` |
| `/mnt` | Mount point for external/temporary filesystems |

---

### File Permissions

Every file/directory has permissions for 3 user classes:

```
-rwxr-xr--
 ||||||||| 
 |||||||++-- others: r--  (read only)
 ||||+++---- group:  r-x  (read + execute)
 |+++------- owner:  rwx  (full)
 +---------- type: - = file, d = directory, l = symlink
```

| Permission | Letter | Octal |
|---|---|---|
| Read | r | 4 |
| Write | w | 2 |
| Execute | x | 1 |

**Common octal values:**
- `7` = rwx (4+2+1)
- `6` = rw- (4+2)
- `5` = r-x (4+1)
- `4` = r-- (4)

---

### `chmod` — Change File Permissions

**Symbolic mode:**
```bash
chmod u+x file        # add execute for owner
chmod g+x,o+x file   # add execute for group and others
chmod o-x file        # remove execute from others
chmod a+r file        # add read for all (a = all)
chmod a-r file        # remove read from all
chmod -R o+x dir/     # recursive: apply to all files in directory
chmod --reference=file1 file2  # copy permissions from file1 to file2
```

**Octal mode:**
```bash
chmod 644 file    # owner: rw-  group: r--  others: r--  (standard file)
chmod 754 file    # owner: rwx  group: r-x  others: r--
chmod 500 file    # owner: r-x  group: ---  others: ---
chmod 700 dir/    # owner: rwx  group: ---  others: ---  (private dir)
```

---

### `ls` — Listing Files

```bash
ls -a         # show hidden files (dot files)
ls -l         # long format (permissions, owner, size, date)
ls -lh        # long format with human-readable sizes (KB, MB)
ls -dl */     # info on directories themselves (not their contents)
ls -R         # recursive — list all subdirectories
ls -lah       # combine: long + all + human-readable
```

---

### `cp` — Copy Files

```bash
cp file1 dir/             # copy file1 into dir
cp -r dir1/ dir2/         # copy directory recursively
cp *.txt dir/             # copy all .txt files
```

---

### `mv` — Move / Rename Files

```bash
mv file dir/              # move file into directory
mv dir1/ dir2/            # rename directory
mv file1.txt file2.txt    # rename file
mv *.txt dir/             # move all .txt files
mv -v *.txt ../dir/       # verbose: show what's being moved
```

**mv options:**
```bash
mv -i file dir/    # interactive: ask before overwriting
mv -u file dir/    # only move if source is newer than target
mv -n file dir/    # no-clobber: never overwrite
mv -b file dir/    # backup: rename old file if overwritten
```

---

### Linux 101 Commands

| Command | What it does |
|---|---|
| `man cmd` | manual page for any command |
| `file name` | detect file type (doesn't rely on extension) |
| `cat file` | print file contents |
| `less file` | scroll through file (q to quit) |
| `head -n 5 file` | first 5 lines |
| `tail -n 5 file` | last 5 lines |
| `grep "word" file` | search for pattern in file |
| `wc -l file` | count lines |
| `sort file` | sort lines alphabetically |
| `uniq` | remove duplicate adjacent lines (pipe after sort) |
| `echo "text"` | print text to terminal |
| `cmd1 \| cmd2` | pipe: send output of cmd1 to cmd2 |
| `cmd > file` | redirect output to file (overwrites) |
| `cmd >> file` | redirect output to file (appends) |
| `apropos word` | search man pages by keyword |
| `whereis cmd` | find binary, source, man page location |
| `which cmd` | show path of the command that would run |
| `find / -name file 2>/dev/null` | find file, suppress permission errors |
| `whoami` | current username |
| `id` | user ID, group ID, group memberships |
| `who` / `w` | who is logged in |
| `last` | login history |
| `uptime` | how long system has been running |
| `uname -a` | kernel/system info |
| `hostname` | system hostname |
| `pwd` | current working directory |
| `history` | command history |
| `top` | live process viewer |
| `dmesg \| more` | kernel ring buffer (boot messages) |
| `cal` | calendar |
| `date` | current date/time |
| `clear` | clear terminal |

---

### Exercises — Session 2.5

**2.5.a — Filesystem research:** explain each directory listed above (see table)

**2.5.b — Linux 101:** practice every command in the table above

**2.5.c — Misc commands to try:**
```bash
echo "danmark er dejligt"
passwd              # change password
date / hostname / arch / uname -a
whoami / who / id / pwd / w
uptime / top / last
dmesg | more
echo $SHELL         # which shell am I using?
history
cal / cal 2022 / cal 9 2022
find / -type f -name ifconfig 2>/dev/null
```

**2.5.d — cp exercises:**
```bash
mkdir -p /exercise2.5/test1 /exercise2.5/test2
# create some .txt files in test2
cp /exercise2.5/test2/file1.txt /exercise2.5/test1/
cp -r /exercise2.5/test2/ /exercise2.5/test1/
cp /exercise2.5/test1/*.txt /exercise2.5/test2/
```

**2.5.e — mv exercises:**
```bash
mv /exercise2.5/test2/*.txt /exercise2.5/test1/
mv /exercise2.5/test1/a* /exercise2.5/test2/
mv -uv /exercise2.5/test2/* /exercise2.5/test1/   # only if newer
mv -bv /exercise2.5/test1/* /exercise2.5/test2/   # backup on overwrite

# Rename all files starting with "a" → "bob..."
for f in a*; do mv "$f" "bob${f#a}"; done

# Rename all files containing "1" → replace with "one"
for f in *1*; do mv "$f" "${f//1/one}"; done

rm filename         # remove file
rm -r dirname/      # remove directory recursively
```

---

### Key Concepts for Exam

- **CIA triad:** Confidentiality (no unauthorized reading), Integrity (no unauthorized modification), Availability
- **Disk encryption** protects against physical access attacks — OS controls alone are not enough
- **Sudo** gives controlled, accountable privilege escalation without sharing root
- **Privilege separation** limits blast radius if an account is compromised
- **Principle of Least Privilege** — users/admins should only have exactly the access they need
- **`visudo`** — always use it to edit sudoers, never edit the file directly