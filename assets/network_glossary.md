# Network Glossary with Metaphors 🌐

## 📚 THE 5-LAYER MODEL (TCP/IP)

### Layer 5: Application Layer

**What it is:** Where user applications and network services operate (HTTP, DNS, SMTP, etc.)  
**Metaphor:** The **"restaurant menu"** - what you actually want to order (web pages, emails, files)  
**Port examples:** HTTP=80, HTTPS=443, DNS=53, SMTP=25, SSH=22

### Layer 4: Transport Layer

**What it is:** Handles end-to-end communication between applications (TCP/UDP)  
**Metaphor:** The **"delivery service"** - decides how your package gets delivered (reliable courier vs. drone drop)  
**Key protocols:** TCP (reliable, ordered) and UDP (fast, unreliable)

### Layer 3: Network Layer

**What it is:** Routes packets across networks using IP addresses  
**Metaphor:** The **"postal system"** - figures out which roads to take to reach the destination address  
**Key protocols:** IPv4, IPv6, ICMP

### Layer 2: Data Link Layer

**What it is:** Manages communication between directly connected devices using MAC addresses  
**Metaphor:** The **"local courier"** - delivers within your neighborhood/building  
**Key protocols:** Ethernet, WiFi (802.11), ARP

### Layer 1: Physical Layer

**What it is:** The actual physical medium (cables, radio waves)  
**Metaphor:** The **"roads and cables"** - the physical infrastructure

---

## 📦 ENCAPSULATION (BY HEART!)

**What it is:** Each layer adds its own header as data moves down the stack  
**Metaphor:** **Russian nesting dolls** - each layer wraps the previous one

- **Layer 5:** Message (M)
- **Layer 4:** Segment (H + M)
- **Layer 3:** Datagram (H + H + M)
- **Layer 2:** Frame (H + H + H + M)
- **Layer 1:** Bits (H + H + H + H + M)

---

## 🔌 KEY CONCEPTS

### Protocol

**What it is:** Set of rules defining how systems communicate  
**Metaphor:** **"Language and etiquette"** - agreed-upon rules so everyone understands each other  
**Example:** HTTP defines how browsers request web pages

### Socket

**What it is:** Endpoint for sending/receiving data (IP + Port)  
**Metaphor:** **"Door with an address"** - specific entrance to a building (IP) and apartment number (port)  
**Format:** 192.168.1.1:80 (IP:Port)

### Port Number

**What it is:** 16-bit number identifying specific application/service (0-65535)  
**Metaphor:** **"Apartment number"** - which specific room in the building to deliver to  
**Remember:** Lower numbers (0-1023) are "well-known" reserved ports

---

## 🚛 TRANSPORT LAYER

### TCP (Transmission Control Protocol)

**What it is:** Reliable, connection-oriented, in-order delivery  
**Metaphor:** **"Certified mail with tracking"** - guaranteed delivery, signed receipt, arrives in order  
**Key features:**

- 3-way handshake (SYN → SYN/ACK → ACK)
- Flow control (don't overwhelm receiver)
- Congestion control (don't overwhelm network)
- Reliable (retransmits lost packets)

### UDP (User Datagram Protocol)

**What it is:** Unreliable, connectionless, no guarantees  
**Metaphor:** **"Postcard in the mail"** - fast, cheap, but might get lost or arrive out of order  
**Use cases:** Live streaming, DNS, DHCP (when speed > reliability)

### 3-Way Handshake

**What it is:** TCP connection setup process  
**Metaphor:** **"Phone call greeting"**

- Client: "Hello?" (SYN)
- Server: "Hello! I hear you!" (SYN/ACK)
- Client: "Great, let's talk!" (ACK)

![3 way handshake with http request and response, data packets loss and SACK permitted](3wayhandshake_httpreq_sack.svg)

### Sequence Number

**What it is:** Number tracking position in data stream  
**Metaphor:** **"Page numbers in a book"** - reassemble pages in correct order even if they arrive mixed up  
**Size:** 32-bit (0 to ~4 billion)

### Multiplexing/Demultiplexing

**What it is:** Multiple applications sharing one network connection  
**Metaphor:** **"Apartment mailboxes"** - one building entrance, but mail sorted to individual boxes  
**How:** Uses port numbers to direct data to correct application

---

## 🌐 NETWORK LAYER

### IP Address

**What it is:** 32-bit identifier for network interface (IPv4)  
**Metaphor:** **"Street address"** - unique location on the network  
**Format:** 192.168.1.1 (four octets, each 0-255)

### Interface

**What it is:** Connection point between device and network  
**Metaphor:** **"Network port on your computer"** - physical or virtual connection point  
**Note:** Routers have multiple interfaces, hosts usually have 1-2

### Subnet

**What it is:** Group of devices sharing the same network prefix  
**Metaphor:** **"Neighborhood"** - houses that can talk directly without going through city center (router)  
**Example:** 192.168.1.0/24 (first 24 bits = network, last 8 bits = hosts)

### CIDR (Classless InterDomain Routing)

**What it is:** Notation showing network prefix length  
**Metaphor:** **"Zip code precision"** - /24 is like a neighborhood, /16 is like a city  
**Format:** 200.23.16.0/23 (first 23 bits are network part)

### Subnet Mask

**What it is:** The /XX number defining network vs. host bits  
**Metaphor:** **"Area code for phone numbers"** - defines which part is the network  
**Remember:** /24 = first 24 bits are network, last 8 bits for hosts (256 addresses)

### IP Datagram

**What it is:** Network layer packet (like "segment" in transport layer)  
**Metaphor:** **"Package with shipping label"** - contains headers and payload  
**Max size:** 1500 bytes (MTU - Maximum Transmission Unit)

### Fragmentation

**What it is:** Splitting large packets into smaller pieces  
**Metaphor:** **"Breaking up IKEA furniture"** - too big for one box, split into multiple packages  
**Fields:** 16-bit identifier (same for all fragments), fragment offset (position)

### TTL (Time To Live)

**What it is:** Hop counter that decrements at each router  
**Metaphor:** **"Expiration date"** - packet dies after X hops to prevent infinite loops  
**Remember:** NOT time-based! It's a hop counter (not seconds)  
**Use:** traceroute exploits TTL to map network paths

### Forwarding

**What it is:** Moving packets from input to output port  
**Metaphor:** **"Traffic cop at intersection"** - directing cars which way to go  
**Layer:** Data plane operation

### Routing

**What it is:** Determining the path from source to destination  
**Metaphor:** **"GPS calculating route"** - planning the entire journey  
**Layer:** Control plane operation

---

## 🏠 IP ADDRESS ASSIGNMENT

### DHCP (Dynamic Host Configuration Protocol)

**What it is:** Automatically assigns IP addresses to devices  
**Metaphor:** **"Hotel check-in desk"** - gives you a room number when you arrive  
**Ports:** UDP 67 (server), 68 (client)

### DORA Process (DHCP)

**What it is:** 4-step DHCP process  
**Metaphor:** **"Looking for a hotel room"**

- **D**iscover: "Any hotels available?" (broadcast)
- **O**ffer: "Yes! Room 203 is free!" (broadcast)
- **R**equest: "I'll take room 203!" (broadcast)
- **A**ck: "Confirmed! Here's your key!" (broadcast)  
  **Why broadcast?** Client has no IP yet!

### NAT (Network Address Translation)

**What it is:** One public IP for entire local network  
**Metaphor:** **"Company receptionist"** - all calls go through one number, receptionist routes to correct extension  
**Example:** Home router (10.0.0.x) appears as one public IP to internet  
**Note:** Breaks layering (uses port numbers from transport layer)

---

## 📧 APPLICATION LAYER PROTOCOLS

### HTTP (HyperText Transfer Protocol)

**What it is:** Protocol for web pages  
**Metaphor:** **"Restaurant order system"** - request menu (GET), place order (POST)  
**Port:** 80 (HTTP), 443 (HTTPS)  
**Type:** Stateless, request/response

### Persistent vs Non-Persistent Connections

**Persistent:** Multiple objects over one TCP connection (HTTP/1.1)  
**Metaphor:** **"Keep phone line open"** - multiple questions in one call  
**Non-Persistent:** One object, then close (HTTP/1.0)  
**Metaphor:** **"Hang up and call back"** - one question per call

### Cookies

**What it is:** Small data stored by browser  
**Metaphor:** **"Loyalty card with your ID"** - remembers who you are between visits  
**Types:** Persistent (saved after closing) vs. Session (deleted when browser closes)

### DNS (Domain Name System)

**What it is:** Translates domain names to IP addresses  
**Metaphor:** **"Phone book"** - looks up name to find number  
**Port:** 53 (UDP, sometimes TCP)  
**Structure:** Root → TLD (.com) → Authoritative (specific domain)

### DNS Query Types

**Recursive:** "Find it for me and tell me" (I wait while you ask others)  
**Iterative:** "Tell me who to ask next" (I do the work)  
**Metaphor:** Recursive = **"Personal assistant"**, Iterative = **"Getting directions"**

### DNS Record Types

- **A Record:** Domain → IPv4 address  
  **Metaphor:** "Home address in phone book"
- **AAAA Record:** Domain → IPv6 address  
  **Metaphor:** "New-style address format"
- **CNAME:** Alias → Real name  
  **Metaphor:** "Nickname pointing to real name"
- **NS:** Domain → Authoritative name server  
  **Metaphor:** "Who's in charge of this area?"
- **MX:** Domain → Mail server  
  **Metaphor:** "Where to deliver mail for this address"

### SMTP (Simple Mail Transfer Protocol)

**What it is:** Protocol for sending email  
**Metaphor:** **"Post office conversation"** - polite exchange when handing over mail  
**Port:** 25 (TCP)  
**Type:** Push protocol (direct transfer)  
**Phases:** Handshake → Transfer → Closure

---

## 🧊 ICMP (Internet Control Message Protocol)

### ICMP

**What it is:** Error reporting and diagnostics (ping, traceroute)  
**Metaphor:** **"Postal service return letters"** - "destination unreachable", "package too big"  
**Layer:** Network layer (but sits "above" IP)  
**Uses:** Ping (echo request/reply), error messages

### Traceroute

**What it is:** Maps network path by exploiting TTL  
**Metaphor:** **"Breadcrumb trail"** - leave markers at each hop to see the route  
**How it works:**

1. Send packets with TTL=1, 2, 3...
2. Each router sends back "TTL expired" with its address
3. Destination sends "port unreachable" (we're done!)

---

## 🌟 IPv6

### IPv6

**What it is:** Next generation IP with 128-bit addresses  
**Metaphor:** **"Moving from apartment building to entire city"** - vastly more addresses  
**Why:** IPv4 running out of addresses (32-bit = ~4 billion)  
**Header:** Fixed 40-byte header (simpler, faster)

### IPv6 Tunneling

**What it is:** Carrying IPv6 inside IPv4 packets  
**Metaphor:** **"Package inside a package"** - new envelope format wrapped in old format  
**Why:** Can't upgrade all routers simultaneously

---

## 📊 TCP/UDP HEADERS

### TCP Segment Structure

**Source/Dest Port:** 16 bits each (which apps communicate)  
**Sequence Number:** 32 bits (page number for ordering)  
**Acknowledgment Number:** 32 bits (received up to this page)  
**Flags:** SYN, ACK, FIN, RST, PSH, URG  
**Window Size:** 16 bits (flow control - how many bytes I can receive)  
**Checksum:** Error detection (basic verification)

### TCP Flags

**Metaphor:** **"Traffic signals"**

- **SYN:** "Let's start" (synchronize)
- **ACK:** "Got it" (acknowledge)
- **FIN:** "I'm done" (graceful close)
- **RST:** "Emergency stop!" (reset connection)
- **PSH:** "This is one complete thing" (push)

### UDP Segment Structure

**Much simpler than TCP:**

- Source Port (16 bits)
- Dest Port (16 bits)
- Length (16 bits)
- Checksum (16 bits)  
  **Metaphor:** **"Postcard"** - minimal wrapping, just send it

---

## 🎯 KEY DIFFERENCES

### TCP vs UDP

| Feature      | TCP                             | UDP                          |
| ------------ | ------------------------------- | ---------------------------- |
| Reliability  | Reliable                        | Unreliable                   |
| Connection   | Connection-oriented (handshake) | Connectionless               |
| Ordering     | In-order delivery               | No ordering                  |
| Speed        | Slower (overhead)               | Faster (minimal overhead)    |
| Use cases    | Web, email, file transfer       | Streaming, gaming, DNS, DHCP |
| **Metaphor** | **Certified mail**              | **Postcard**                 |

---

## 🔧 USEFUL COMMANDS & TOOLS

### nslookup

**What it does:** DNS lookup tool  
**Examples:**

- `nslookup www.kallas.dk` (get IP)
- `set type=NS` (get authoritative name servers)
- `set norecurse` (iterative query)

### dig

**What it does:** More detailed DNS lookup

### traceroute

**What it does:** Shows network path with hop-by-hop RTT

### telnet

**What it does:** Connect to port and send raw commands  
**Example:** `telnet www.kallas.dk 80` then `GET /index.html HTTP/1.1`

### netcat (nc)

**What it does:** Network swiss army knife  
**Example:** `echo "GET / HTTP/1.1\r\nHost: www.kallas.dk\r\n\r\n" | nc www.kallas.dk 80`

---

## 💡 EXAM TIPS

**Must know by heart:**

- 5-layer model with protocols
- Encapsulation (Message → Segment → Datagram → Frame → Bits)
- TCP vs UDP differences
- 3-way handshake (SYN → SYN/ACK → ACK)
- DHCP DORA process
- Common port numbers (HTTP=80, HTTPS=443, DNS=53, SMTP=25, SSH=22)
- What /24 means in CIDR
- How NAT works
- TCP segment structure

**Key metaphors to remember:**

- Layers = "Restaurant experience" (menu → delivery → postal → local courier → roads)
- Encapsulation = "Russian nesting dolls"
- TCP = "Certified mail"
- UDP = "Postcard"
- NAT = "Company receptionist"
- DNS = "Phone book"
- DHCP = "Hotel check-in"
- Sockets = "Doors with addresses"
- TTL = "Expiration date"

---

## ⚠️ COMMON EXAM TRAPS

1. **TTL is NOT time!** It's a hop counter
2. **DHCP uses UDP** (not TCP) - needs to broadcast
3. **NAT breaks layering** - uses ports (transport layer) in network layer
4. **/24 means network portion** (not host count) - first 24 bits
5. **HTTP is stateless by default** - cookies add state
6. **DNS port 53** - UDP normally, TCP for large transfers
7. **Max segment size TCP = 1460 bytes** (1500 MTU - 20 IP header - 20 TCP header)
8. **Sequence numbers are random** (not starting from 0)
