User Management & Authentication
Limiting Login Capabilities
User account details are stored in /etc/passwd and /etc/shadow.
Method 1: Change login shell to nologin
bashusermod -s /usr/sbin/nologin user1

Accounts without a shell: nobody, _apt, whoopsie
Restore shell: usermod -s /bin/bash user1

Method 2: Lock/unlock via passwd
bashpasswd -l user1   # lock
passwd -u user1   # unlock
passwd -S user1   # check status

Locking adds a ! prefix to the hash in /etc/shadow

Method 3: Lock/unlock via usermod
bashusermod -L user1  # lock
usermod -U user1  # unlock
Why lock instead of delete?

Preserves files and ownership
Preserves audit trail / log history
Temporary measure (e.g. employee on leave, investigation)
Allows easy re-enabling


Monitoring User Activity (acct)
acct is an open-source tool for monitoring user activity on Linux.
bashsudo apt-get install acct
ac – login time
bashac           # total login time (all users)
ac -d        # login time per day
ac -p        # login time per user
ac user1     # login time for specific user
lastcomm – commands executed
bashlastcomm         # all users
lastcomm user1   # specific user

Authentication Factors
Three types, from weak to strong:
FactorTypeExampleWhat you knowKnowledgePassword, PINWhat you havePossessionUSB token, phone, smart cardWhat you areInherenceFingerprint, face, voice

2FA = two different factors — two passwords is NOT 2FA
A second factor must be from a different category


PAM (Pluggable Authentication Module)
PAM is the Linux framework for authentication. It allows modular configuration of how users authenticate.
Relevant config files:

/etc/pam.d/common-auth – defines the auth stack
/etc/security/pam_usb.conf – config for USB token module

PAM control flags:

required – must pass; failure continues stack but ultimately fails
sufficient – if passes, no further checks needed
optional – result is ignored unless it's the only module

Physical token options:

USB device – pamusb (works on Ubuntu ≤22.04 with older package)
Mobile app – Google Authenticator via libpam-google-authenticator

Tradeoffs of standard vs. specialized HW:

Standard HW (USB stick, phone) → attacker can duplicate
Specialized/proprietary HW → harder to copy, but more expensive