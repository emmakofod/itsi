Session 13 – System Infection & Ransomware

📌 Key Concepts
Three types of system infection

Rootkits — hide themselves deep in the OS, often in the kernel
Ransomware — encrypts your data and demands payment for the key
Virus and other — general malware category


The 3-step defence model (ideally)

Prevent infection from happening
Detect/discover that infection has occurred
Recover from the infection


The goal is to handle all three — but ransomware forces us to think hardest about step 3: recovery.


🔒 Ransomware
What is it?

One of the most successful types of malware — generates massive revenue for criminals
Encrypts files on the victim's system (and often spreads laterally to network shares, backups, etc.)
Attacker holds the decryption key and demands payment (usually crypto) to return it

How it typically gets in

Phishing emails with malicious attachments or links
Exploiting unpatched vulnerabilities (RDP, VPN, software)
Compromised supply chain software (e.g. REvil/Kaseya attack)
Drive-by downloads

Real-world example — Nevada State Government (2025)

RVTools malware downloaded by one employee
Attackers had one month undetected to add persistence mechanisms
They did not pay the ransom — but recovery cost $1.5 million
Shows the value of: EDR, email security, boundary protection, user awareness training


🛡️ Defence layers (from slides)
Normal system hardening helps but is not enough by itself:

Encrypted disks
Eliminating unnecessary services/software
Admin rights separation
Proper ACLs and user login rights
Host firewall
Network segmentation
Intrusion detection
Logging and monitoring

The most important addition for business continuity: backups.

💾 Recovery — the backup problem
The value of a system = its data + business apps + the OS/HW that manages it.
To recover you need both:
HW/OS recovery:

A "hot standby" — preconfigured spare ready to start immediately
Or a backup image to restore on a generic machine (slower)

Data/application recovery:

Preconfigured application + clean backup data
Critical question: is the infection included in the backup?

The sandbox check

If time allows, run the backup in a sandbox environment first:

Verify it contains the newest possible data
Detect if the backup itself is infected — ransomware often sits dormant before triggering



🔑 Key principle

"What is most effective for business continuation?"
→ Offline, immutable, tested backups that the ransomware cannot reach or encrypt.

The 3-2-1 backup rule:

3 copies of data
2 different storage types
1 copy offsite (or air-gapped)