# System Security – Notes 11
## Host Network Security & iptables

---

## Hvad er en Firewall?

En firewall er et **packet filter** – den inspicerer netværkspakker og beslutter om de skal tillades eller blokeres, baseret på regler.

| Spørgsmål | Svar |
|---|---|
| Hvad er en firewall? | Et packet filter der kontrollerer netværkstrafik |
| Hvad bruges den til? | Blokere/tillade trafik baseret på IP, protokol og port |
| Hvad er den IKKE? | En garanti – den ser ikke på data-indholdet (layer 3/4 kun) |

---

## Host Network Contact Area

- En **host** = en server på netværket
- Serveren har **network interfaces** der forbinder den til nettet
- Disse interfaces er entry/exit points → dem skal vi beskytte
- Beskyttelse sker via **host firewall** (iptables)

---

## Manuel TCP/IP Konfiguration

Servere bruger typisk **statisk IP** i stedet for DHCP.

**Hvorfor ikke DHCP på servere?**
- DHCP giver skiftende IP → upålidelig for services der skal nås konsistent
- Statisk IP sikrer forudsigelighed og kontrol

**Kommandoer til at tjekke IP:**

```bash
ip address          # Foretrukket moderne kommando
ifconfig            # Ældre alternativ (deprecated)
networkctl status
lshw -class network
```

**Netplan konfiguration (Ubuntu):**

```bash
# Flyt eksisterende config til backup
sudo mv /etc/netplan/00-*.yaml /etc/netplan/00-*.bak

# Opret ny config
sudo nano /etc/netplan/10-config.yaml
```

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    ens33:
      addresses:
        - 192.168.249.101/24
      routes:
        - to: default
          via: 192.168.249.2
      nameservers:
        addresses: [192.168.249.2, 8.8.8.8]
```

```bash
sudo netplan apply   # Aktivér konfigurationen
```

---

## iptables – Host Firewall

### De tre chains

| Chain | Funktion |
|---|---|
| `INPUT` | Indkommende trafik **til** hosten |
| `FORWARD` | Trafik der routes **igennem** hosten til andet destination |
| `OUTPUT` | Udgående trafik **fra** hosten |

### Grundlæggende kommandoer

```bash
iptables -V          # Tjek version
iptables -L          # List regler (simpel)
iptables -L -v       # List regler (verbose)
iptables -S          # List regler som kommandoer
```

### Filosofi: Block-all vs Allow-all

> **Anbefalet strategi: Block ALL → Allow KNOWN**

| Strategi | Fordel | Ulempe |
|---|---|---|
| Blokér dårlig trafik, tillad resten | Enkel at sætte op | Ukendte angreb slipper igennem |
| Blokér ALT, tillad kun kendte | Stærkest mulig beskyttelse | Kræver omhyggelig konfiguration |

---

## Opsætning af iptables – Step by Step

### 1. Tillad loopback (localhost)
```bash
sudo iptables -I INPUT 1 -i lo -j ACCEPT
```

### 2. Tillad etablerede/relaterede forbindelser
```bash
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
```
> Accepterer svar på udgående forbindelser (fx SSH, SCP, FTP)

### 3. Tillad SSH (inden du låser dig ude!)
```bash
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
# Hvis SSH er på anden port:
sudo iptables -A INPUT -p tcp --dport 22123 -j ACCEPT
```

### 4. ICMP regler

```bash
# Type 8  = Echo Request (ping)
iptables -A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT

# Type 11 = Time Exceeded (holder tidsbegrænsede forbindelser aktive)
iptables -A INPUT -p icmp -m icmp --icmp-type 11 -j ACCEPT

# Type 3  = Destination Unreachable
iptables -A INPUT -p icmp -m icmp --icmp-type 3 -j ACCEPT
```

### 5. Custom chain

```bash
iptables -N ALLOWED               # Opret ny chain
iptables -A INPUT -j ALLOWED      # Send INPUT trafik til ALLOWED chain

iptables -A ALLOWED -p tcp --dport 22 -j ACCEPT   # SSH
iptables -A ALLOWED -p tcp --dport 80 -j ACCEPT   # HTTP
iptables -A ALLOWED -p tcp --dport 443 -j ACCEPT  # HTTPS
```

### 6. Drop/Reject alt andet

```bash
# DROP – pakken smides væk, ingen svar
sudo iptables -A INPUT -j DROP

# REJECT – pakken afvises med ICMP fejlbesked
sudo iptables -A INPUT -j REJECT --reject-with icmp-host-unreachable
```

> **Forskel på DROP vs REJECT:**
> - `DROP` → tavs afvisning, angriber ved ikke om host eksisterer
> - `REJECT` → sender fejlbesked tilbage, hurtigere feedback til legit fejl

### 7. Tillad specifik IP-range

```bash
# Eksempel: kun trafik fra internt netværk til port 3306 (MySQL)
iptables -A INPUT -s 192.168.1.0/24 -p tcp --dport 3306 -j ACCEPT
```

### 8. Gem regler (overlever reboot)

```bash
sudo apt install iptables-persistent
sudo iptables-save > /etc/iptables/rules.v4
```

---

## Application Layer Filtering

| | Layer 3/4 Filtering (iptables) | Application Layer Filtering |
|---|---|---|
| Ser på | IP, protokol, port | Selve data-indholdet i pakkerne |
| Eksempel | Blokér port 80 | Inspicér HTTP request indhold |
| Airport-analogi | Pas, destination, gate | Undersøgelse af bagagen |
| Kostbarhed | Billig og hurtig | Dyr, kræver applikationsviden |

> Layer 7 filtering bruges sjældent i praksis – for ressourcekrævende. De fleste er tilfredse med layer 3/4.

---

## Øvelse 11.1 – iptables regler

Se separat øvelsesnoter.

---

## Øvelse 11.2 – Argumentation

**Spørgsmål:** Hvorfor skal en host have sin egen iptables, selvom virksomhedens gateway-FW allerede beskytter?

**Argument (defense in depth):**
- Gateway FW beskytter mod **ekstern** trafik, men ikke intern
- Intern trafik (kompromitteret kollega, malware på LAN) slipper forbi gateway FW
- En host-baseret firewall begrænser **lateral movement** ved et angreb
- Hvert system har unikke services → individuelle regler giver mindst mulig angrebsflade
- **"It's a network problem. Talk to Dany."** er et ansvarsfralæggelse – system defenders ejer også host-sikkerhed

---

## Eksamensrelevant Summary

| Begreb | Forklaring |
|---|---|
| iptables | Linux packet filter til host firewall |
| Chain INPUT | Regler for indkommende trafik |
| Chain OUTPUT | Regler for udgående trafik |
| Chain FORWARD | Regler for trafik der routes videre |
| ACCEPT | Tillad pakken |
| DROP | Smid pakken (ingen svar) |
| REJECT | Afvis pakken med ICMP fejl |
| conntrack | Sporer forbindelsesstatus (ESTABLISHED, RELATED) |
| iptables-persistent | Pakke til at gemme regler på tværs af reboots |
| Netplan | Ubuntu's netværkskonfigurationsværktøj (YAML) |
| Defense in depth | Lag-på-lag sikkerhed – host FW + gateway FW |
| Layer 3/4 vs Layer 7 | iptables = IP/transport; app-proxy = applikationsdata |