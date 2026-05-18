# Session 17 : IT Security Policy Framework

## Hvorfor hænger dette sammen med resten af kurset?

Alt vi har lært i session 1–16 er teknisk
Men teknisk arbejde uden dokumentation er ingenting
Hvis du ikke kan sætte dit arbejde ind i en ELI5 kontekst, er du ikke størk nok i det.

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