# Session 17 : IT Security Policy Framework

## Hvorfor hænger dette sammen med resten af kurset?

Alt vi har lært i session 1–16 er teknisk
Men teknisk arbejde uden dokumentation er ingenting
Session 17 er svaret på: hvad er meningen med det hele?

## Policy, Standards og Procedures : hvad er forskellen?

De tre niveauer hænger sammen men er ikke det samme:

**Policy** er det øverste niveau og ejes af ledelsen. Det handler om *hvad* der skal beskyttes og *hvorfor*. Ikke teknik. Et policy-dokument er kort og skrevet i forretningssprog. Det besvarer:
- Hvilke data har vi?
- Hvad er de værd for virksomheden?
- Hvad sker der hvis de kompromitteres?
- Hvad skal beskyttes mod hvad?

**Standards** er det tekniske niveau. IT Security analyserer *hvordan* policyen opfyldes og hvad det koster. Ledelsen godkender. Indeholder "musts" og "shoulds" med budgetter. Det er stadig ikke en step-by-step guide : det er retningslinjer og krav.

**Procedures** er det operationelle niveau. Skrevet af IT-folk til IT-folk. Specifikt nok til at en hvilken som helst uddannet person kan følge dem. Ikke vage ord, ikke links til eksterne lister. Eksempel på en rigtig procedure:

> "Rediger /etc/ssh/sshd_config. Sæt PermitRootLogin no. Sæt PasswordAuthentication no. Sæt AllowGroups sshusers. Genindlæs med systemctl reload ssh. Verificer med sshd -T | grep permitrootlogin."

Det er en procedure. "Harden SSH" er ikke en procedure : det er et mål.

## Hvorfor starte med dataklassifikation?

Data er det vi i virkeligheden beskytter. Alt andet (servere, netværk, firewalls) eksisterer for at beskytte data. Hvis man ikke ved hvad man har og hvad det er værd, kan man ikke træffe rationelle sikkerhedsbeslutninger.

Typisk klassifikation:
- **Public** : kan deles frit
- **Internal** : kun til ansatte
- **Restricted** : fortroligt, begrænset adgang

Fra dataklassifikation bestemmer man hvilke applikationer der håndterer det, hvilke databaser der gemmer det, hvilke servere der kører det, og hvilke netværkszoner det befinder sig i. Alt dette styrer sikkerhedskravene.

## Planned insecurity : hvad betyder det?

Der er ingen absolut sikkerhed. Det er en fælde at fortælle ledelsen "vi er sikre." Den rigtige tilgang er: *hvilken risiko accepterer vi, og hvilken mitigerer vi?*

Det er en forretningsbeslutning, ikke en teknisk beslutning. Ligesom en bank ikke bygger det mest sikre pengeskab i verden fordi det ville gøre det umuligt at drive bank. Der er altid en afvejning.

Pointet: ledelsen skal beslutte risikoaccepten. IT Security hjælper dem med at forstå hvad de beslutter.


## Hvorfor skal procedures vedligeholdes?

En procedure fra 2022 kan være forkert i 2026. Nye sårbarheder opdages, software opdateres, serverroller ændrer sig. Hvis procedures ikke opdateres løbende:

- En ny admin følger en forældet guide og konfigurerer forkert
- Auditorer (ISO 27001, NIS2) godkender ikke udaterede dokumenter
- Efter et sikkerhedsincident aner man ikke om proceduren var fulgt : fordi den ikke var opdateret

Treat it like code: versionsstyret, reviewed, opdateret efter incidents.


## Forbindelsen til resten af kurset


Session 1 : CIA triad, hash-verificering: Policy definerer hvad der skal beskyttes og hvorfor. Uden en policy ved ingen hvad der er vigtigt.

Session 2 : LUKS, sudo: Standards siger "alle laptops og servere skal krypteres" og "ingen deler root-adgang."

Session 3 : Nmap: Procedures siger hvornår og hvordan man scanner sit eget netværk : og hvad man gør ved det man finder.

Session 4 : Metasploit: Standards kræver patching. Procedures siger hvornår, hvem der gør det, og hvordan det dokumenteres.

Session 5 : ACL: Standards definerer adgangsniveauer per afdeling. Procedures siger præcis hvilke ACL-regler der sættes på hvilke mapper.

Session 6 : LDAP: Standards siger "central brugeradministration." Procedures siger hvordan brugere oprettes, deaktiveres og auditeres.

Session 7 : PAM, 2FA: Standards kræver 2FA på kritiske systemer. Procedures siger hvilke systemer og hvilken metode.

Session 8 : SSH hardening: Procedures siger præcis hvilke linjer der sættes i sshd_config og hvordan det verificeres.

Session 9 : SCP/SFTP, Kerberos: Standards forbyder plaintext filoverførsler. Procedures siger hvilke protokoller der er godkendte.

Session 11 : iptables: Standards definerer default-deny. Procedures definerer hvilke porte der åbnes på hvilke servertyper.

Session 12 : Tripwire, PortSentry, Squid: Procedures siger hvornår Tripwire-baseline tages og hvordan afvigelser håndteres.

Session 13 : Malware, ransomware: Policy definerer hvad der sker ved et angreb. Procedures er incident response-planen.

Session 14–15 : Logging, Lynis: Procedures siger hvornår og hvordan logs gennemgås og hvem der modtager alerts.

Session 16 : Hardening lists: Procedures er den virksomhedsspecifikke hardening-liste - tilpasset, testet og vedligeholdt.

Session 17 binder det hele sammen.




FLERE whys

Why do we have security policies?
- Technology alone cannot protect an organisation. Humans make mistakes,
and a policy defines what is expected so people know what is and isn't allowed.
- Without a policy you cannot hold anyone accountable, and regulators like
GDPR and NIS2 require documented policies. No policy means legal liability.

Why encrypt disks (LUKS)?
- A login password only protects the running OS. If someone steals a laptop
they can boot their own OS and read everything. Disk encryption makes the
data unreadable without the key, even if the physical disk is gone.

Why use sudo instead of sharing root?
- Root can do anything with no restrictions and no audit trail. Sharing root
means no accountability. Sudo gives controlled, logged privilege escalation
and limits the blast radius if an account is compromised.

Why scan your own network (Nmap)?
- You cannot defend what you do not know exists. Every open port is a potential
entry point. Attackers will scan your network anyway, so it is better to find
problems first.

Why study attacks (Metasploit)?
- You can only defend against threats you understand. Metasploit shows that
exploitation is a structured, repeatable process. If you do not know how
something is attacked you cannot make good defence decisions.

Why use ACL on top of standard Linux permissions?
- Standard permissions only allow one owner, one group, and one catch-all for
everyone else. Real organisations need more granularity. ACL lets you give
specific permissions to any number of users or groups independently.

Why centralise user management (LDAP)?
- Without central management, every server has its own user list. Removing an
employee means updating every machine, and it is easy to miss one. With
LDAP, one change applies everywhere instantly.

Why use 2FA and PAM?
- A password can be stolen without the user knowing. 2FA requires something
the attacker also has to physically steal. PAM lets Linux stack different
authentication methods flexibly without rewriting applications.

Why harden SSH?
- SSH exposes authentication to the internet. Default configs allow root login
and use the standard port, which automated bots constantly target. Disabling
root login, changing the port, restricting allowed users, and using key-based
auth instead of passwords all reduce the attack surface significantly.

Why use a host firewall (iptables)?
- A network firewall only protects the perimeter. Once an attacker is inside the
network, for example through phishing, the network firewall does not help.
iptables protects the individual server from other machines on the same
internal network.
- Rule order matters: iptables evaluates rules top-down and stops at the first
match. Default deny is safer than default allow because unknown traffic gets
blocked automatically.

Why use Tripwire, PortSentry, and Squid?
- Tripwire creates a cryptographic baseline of the system so you can detect
exactly which files changed after an incident. Without it you are guessing.
- PortSentry detects port scans, which are almost always reconnaissance
before an attack. Catching it early means you can block the attacker before
they find a vulnerability.
- Squid proxies all outbound web traffic. If malware tries to call home, the proxy
can block it and logs reveal which machines are making unusual requests.

Why log everything, and why log remotely?
- Logs are your time machine after an incident. The Nevada 2025 case showed
attackers went undetected for a month because detection was slow. Better
logging means faster detection, which means smaller blast radius.
- An attacker with root access can delete local logs in one second. Remote logs
on a separate machine cannot be tampered with from the compromised host.
If local and remote logs differ, the difference shows exactly what the attacker
tried to hide.

Why understand malware types?
- Each type requires a different response. A ransomware incident is completely
different from a rootkit incident. Rootkits are the most dangerous because the
compromised OS actively lies to you, and you cannot trust any output from it.
Detection requires booting from a clean external source.
- Paying ransom is not a solution. It funds further attacks and gives no
guarantee of a working decryption key. The real answer is working offline
backups, fast detection, and an incident response plan.

Why make a hardening checklist?
- A pilot does not rely on memory before takeoff. Security hardening has the
same problem: there are 20 to 40 things to configure and humans forget
under pressure. A checklist ensures consistency regardless of who sets up
the server.
- External lists should never be copied blindly. If you do not understand why a
point exists you cannot tell if it applies to your environment or if it is outdated.
Every item must be verified, tested, and adapted.

Why does system security need business alignment (Policy, Standards,Procedures)?
- Technical controls without management support do not get funded or
enforced. Security is often seen as overhead. You need to justify it by showing
risk reduction or regulatory compliance.
- Policy is the what, owned by management. Standards are the how technically,
agreed with management. Procedures are the specific step-by-step
instructions written by IT. Keeping them separate means the right people own
the right decisions.
- Data classification is where everything starts. If you do not know what data
you have and what it is worth, you cannot make rational decisions about how
much to spend protecting it.

The thread through everything
- Principle of least privilege appears in almost every session. Limiting what
each user and process can do means that when something goes wrong, the
damage is contained.
- Defence in depth means no single control is relied on. Perimeter firewall, host
firewall, strong auth, encryption, logging, and monitoring all work together.
One layer failing does not mean everything fails.
- Prevention alone is not enough. The M&S and Nevada cases prove that even
well-protected organisations get breached. Monitoring is what turns a breach
into something you detect in hours instead of months.
