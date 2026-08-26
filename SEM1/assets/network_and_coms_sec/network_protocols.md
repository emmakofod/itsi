# Network Protocols — Reference Document

## The 5-Layer TCP/IP Model

| Layer | Name | Protocols |
|-------|------|-----------|
| 5 | **Application** | HTTP (80), HTTPS (443), DNS (53), SMTP (25), FTP (20/21), SSH (22), NTP (123), DHCP (67/68) |
| 4 | **Transport** | TCP, UDP |
| 3 | **Network** | IPv4, IPv6, ICMP |
| 2 | **Data Link** | Ethernet (802.3), WiFi (802.11), ARP |
| 1 | **Physical** | Cables, fiber *(out of scope)* |

> The OSI model has 7 layers (adds Presentation and Session between App and Transport) — but those are implemented inside the Application layer in practice.

### Encapsulation
Each layer wraps the layer above it with its own header:

```
Layer 5 → Message (M)
Layer 4 → Segment    = [Header | M]
Layer 3 → Datagram   = [Header | Header | M]          ← router level
Layer 2 → Frame      = [Header | Header | Header | M] ← switch level
Layer 1 → Bits       = everything above as raw bits
```

### Most Important Protocols to Know
`HTTP · DNS · DHCP · UDP · IPv4 · IPv6 · ICMP · Ethernet · ARP`

> DNS, DHCP run over **UDP**. HTTP, SMTP run over **TCP**.

---

## Application Layer Protocols

### HTTP — HyperText Transfer Protocol
- **Port:** 80 (TCP)
- **Stateless** — server keeps no memory of past requests
- **Client-server** — client sends request, server sends response
- Runs over TCP (reliable delivery required)

#### HTTP Versions
- **HTTP/1.0** — non-persistent: one object per connection, then closes
- **HTTP/1.1** — persistent: multiple objects over one connection, closes after timeout

#### Cookies
- **Persistent cookies** — stay in browser even after closing
- **Session cookies** — deleted when session ends

#### Request Message Format
```
GET /index.html HTTP/1.1\r\n
Host: www.example.com\r\n
\r\n
```
- **Request line:** method + resource + version
- **Methods:** GET, POST, PUT, DELETE
- **Header lines** follow (Host is mandatory in HTTP/1.1)
- Empty line `\r\n` marks end of headers

#### Response Message Format
```
HTTP/1.1 200 OK\r\n
[headers]\r\n
\r\n
[body]
```

#### Status Codes
| Range | Meaning |
|-------|---------|
| `2xx` | OK / Success |
| `3xx` | Moved / Redirect |
| `4xx` | Client error (404 = Not Found, 401 = Unauthorized) |
| `5xx` | Server error |

#### Try it yourself (Kali)
```bash
telnet www.kallas.dk 80
# then type:
GET /index.html HTTP/1.1
Host: www.kallas.dk
# press Enter twice

# Or with netcat:
echo "GET / HTTP/1.1\r\nHost: www.kallas.dk\r\n\r\n" | nc www.kallas.dk 80
```

---

### DNS — Domain Name System
- **Port:** 53 — **UDP** (primary), TCP (for large responses / zone transfers)
- Translates domain names → IP addresses

#### DNS Hierarchy
1. **Root DNS servers** — 13 worldwide, backbone of the internet
2. **TLD servers** — handle `.com`, `.org`, `.dk`, etc.
3. **Authoritative servers** — hold the actual name → IP mapping for a domain
4. **Local name server** — your ISP's or company's DNS cache

#### Query Types
- **Recursive** — local server asks on your behalf (most common, enables caching)
- **Iterative** — you ask each level yourself (fallback)

#### DNS Record Types
| Type | Description | Example |
|------|-------------|---------|
| **A** | Domain → IPv4 address | `kallas.dk → 165.232.77.195` |
| **AAAA** | Domain → IPv6 address | |
| **CNAME** | Alias → real name (subdomains) | `www.kallas.dk → kallas.dk` |
| **NS** | Domain → authoritative nameserver | |
| **MX** | Mail server for domain (port 25) | |

```bash
nslookup www.kallas.dk              # recursive lookup
nslookup
> set norecurse
> www.kallas.dk                     # iterative lookup
> set type=NS
> www.kallas.dk                     # get nameservers
```

---

### SMTP — Simple Mail Transfer Protocol
- **Port:** 25 (TCP)
- **Push protocol** — direct transfer from sending to receiving mail server
- Encodes binary to **7-bit ASCII**

#### 3 Phases
1. Handshaking (greeting)
2. Transfer of messages
3. Closure

#### Example Interaction
```
S: 220 hamburger.edu
C: HELO crepes.fr
S: 250 Hello crepes.fr, pleased to meet you
C: MAIL FROM: <alice@crepes.fr>
C: RCPT TO: <bob@hamburger.edu>
C: DATA
C: Do you like ketchup?
C: .
S: 250 Message accepted
C: QUIT
```

---

## Transport Layer Protocols

### TCP — Transmission Control Protocol
- **Connection-oriented** — requires 3-way handshake before data
- **Reliable** — no data loss, guaranteed in-order delivery
- **Full-duplex** — both sides can send simultaneously
- **Flow control** — receiver tells sender how much it can handle (receive window)
- **Congestion control** — sender self-regulates based on errors received
- Not secure by default → use **TLS over TCP** for security

#### 3-Way Handshake
```
Client          Server
  |── SYN ────→|   (syn=1, random seq number)
  |←─ SYN/ACK ─|   (server acknowledges + sends own seq)
  |── ACK ────→|   (connection established)
```

#### TCP Segment Header Fields
| Field | Description |
|-------|-------------|
| Source port | Sender's port (0–65535, 2^16) |
| Dest port | Target service (80, 25, 22...) |
| Sequence number | Position in byte stream (0–4 billion, 2^32) |
| Acknowledgment number | Next expected byte from sender |
| Header length | Minimum 20 bytes (5 D-words) |
| **Flags** | SYN (connect), ACK (acknowledge), FIN (close), RST (reset/error), URG, PSH |
| Receive window | Flow control — max bytes receiver will accept |
| Checksum | Basic error check |
| Options | Variable, e.g. MSS (Max Segment Size = **1460 bytes**) |

> Max transfer unit (MTU) = 1500 bytes. TCP header = 20 bytes. IP header = 20 bytes. → **1460 bytes** payload.

---

### UDP — User Datagram Protocol
- **Connectionless** — no handshake, just send
- **Unreliable** — packets may be lost or arrive out of order
- **Fast and lightweight** — no overhead
- Best for: DNS, DHCP, live video/audio streams (speed > reliability)

#### UDP Header (very simple)
```
| Source Port | Dest Port |
| Length      | Checksum  |
| Data...                 |
```

---

## Network Layer Protocols

### IPv4
- **32-bit addresses** (4 bytes) — e.g. `192.168.1.1`
- Written as 4 decimal octets separated by dots
- **Running out** of addresses → reason for IPv6

#### Key IPv4 Header Fields
| Field | Description |
|-------|-------------|
| Version | IP version (4) |
| TTL (Time To Live) | **Hop counter**, not time — decrements by 1 at each router, packet discarded at 0 |
| Protocol | Tells which transport protocol follows (TCP/UDP/ICMP) |
| Source IP | 32-bit sender address |
| Dest IP | 32-bit receiver address |
| Fragment offset | Where this fragment sits in the original datagram |

> Use `traceroute` to see TTL in action (shows each router hop)

---

### IP Addressing & Subnets

#### CIDR Notation
Format: `a.b.c.d/x` — where x = number of bits for the **network part**

```
192.168.1.0/24
→ First 24 bits = network (192.168.1)
→ Last 8 bits   = host (0–255)
→ Supports 254 hosts (0 = network, 255 = broadcast)
```

#### Subnets
A subnet = a network inside a network. Devices on same subnet can reach each other **without a router**.

---

### DHCP — Dynamic Host Configuration Protocol
- **Port:** 67 (server) / 68 (client) — runs over **UDP**
- Also called "plug-and-play" — automatically assigns IP when you join a network

#### What DHCP gives you
1. IP address (temporary lease)
2. Lease time
3. Subnet mask
4. Default gateway (router)
5. DNS server address

#### 4-Step DORA Process
```
Client          Server (broadcast)
  |── DISCOVER ──────────→|   "Is there a DHCP server?"
  |←──────────── OFFER ───|   "Here's an IP you can use"
  |── REQUEST ────────────→|   "I'll take that IP!"
  |←────────────── ACK ───|   "It's yours!"
```
> All 4 steps use **broadcast** because client has no IP yet — can't use unicast

---

### NAT — Network Address Translation
- Allows an **entire local network to share one public IP**
- Router maintains a **NAT translation table** mapping internal IP:port → public IP:port
- At home: your router is the NAT device
- **Breaks TCP/IP layering** (network layer reads transport layer port numbers) — but necessary

```
Internal: 10.0.0.1:3345  ──→  NAT Router  ──→  Public: 138.76.29.7:5001
                                 (table)
Response: 138.76.29.7:5001 ──→  NAT Router  ──→  10.0.0.1:3345
```

---

### IPv6
- **128-bit addresses** (vs 32-bit in IPv4) — solves address exhaustion
- Fixed **40-byte header** (simpler than IPv4)
- **No checksum** — removed to speed up processing at each hop
- **No fragmentation** at router level — handled at endpoints
- **Hop limit** instead of TTL
- **ICMPv6** — extended version of ICMP

#### IPv4 → IPv6 Transition: Tunneling
IPv6 packets are wrapped inside IPv4 datagrams to travel through IPv4-only routers:
```
[IPv6 datagram] → [IPv4 header | IPv6 datagram] → [IPv6 datagram]
```

---

### ICMP — Internet Control Message Protocol
- **Network-layer** protocol carried inside IP datagrams
- Used for **error reporting** and **diagnostics** (ping, traceroute)
- Has Type and Code fields

#### Common ICMP Messages
| Type | Code | Meaning |
|------|------|---------|
| 0 | 0 | Echo **reply** (ping response) |
| 8 | 0 | Echo **request** (ping) |
| 3 | 0 | Destination network unreachable |
| 3 | 1 | Destination host unreachable |
| 3 | 3 | Destination **port** unreachable |
| 11 | 0 | **TTL expired** (used by traceroute) |

#### How `traceroute` Works
1. Sends UDP packets with TTL=1, TTL=2, TTL=3... to destination
2. Each router that decrements TTL to 0 sends back ICMP "TTL expired" (type 11) with its IP
3. When destination reached → returns ICMP "port unreachable" (type 3, code 3) → stop
4. Result: full path of routers with round-trip times

---

## Data Link Layer Protocols

### Ethernet (802.3)
- Wired LAN standard
- Uses **MAC addresses** (48-bit, hardware-level)

### WiFi (802.11)
- Wireless LAN standard
- Multiple variants (802.11a/b/g/n/ac/ax)

### ARP — Address Resolution Protocol
- Resolves IP addresses → MAC addresses on local network
- "Who has IP 192.168.1.1? Tell me your MAC address"

---

## Port Numbers

| Protocol | Port | Transport |
|----------|------|-----------|
| HTTP | 80 | TCP |
| HTTPS | 443 | TCP |
| SSH | 22 | TCP |
| FTP data | 20 | TCP |
| FTP control | 21 | TCP |
| SMTP | 25 | TCP |
| DNS | 53 | UDP (+ TCP) |
| DHCP server | 67 | UDP |
| DHCP client | 68 | UDP |
| NTP | 123 | UDP |