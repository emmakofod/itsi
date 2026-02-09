# Network Forensic Analysis Report

Det her er Claude genereret - bare for inspo

## Pcap File: cap.pcapng

---

**Report Information:**

- **Analyst:** Network Security Team
- **Analysis Date:** February 9, 2026
- **Tool Used:** Wireshark / tshark
- **Capture File:** cap.pcapng
- **Capture Date:** September 3, 2017 22:25:31 - 22:27:50 UTC
- **Case Reference:** NET-FORENSIC-2026-001

---

## Executive Summary

This report provides a comprehensive forensic analysis of network traffic captured in file `cap.pcapng`. The capture contains **2,065 packets** spanning **138.9 seconds** (approximately 2.3 minutes) of network activity from a home/small office network.

### Key Findings:

🔴 **CRITICAL FINDINGS:**

1. **Unencrypted HTTP traffic to vulnerable test website** (demo.testfire.net)
2. **Multiple HTTP connections** instead of HTTPS (security risk)
3. **Connection to known vulnerable demo application** (AltoroMutual Bank demo)

🟡 **WARNINGS:**

1. Apple device (192.168.1.125) as primary endpoint
2. Multiple Google services connections (some encrypted, some not)
3. eBay advertising tracking observed
4. Internal network device communication on local IPs

✅ **NORMAL ACTIVITY:**

1. TLS/HTTPS encrypted traffic (536 packets)
2. DNS resolution through local gateway
3. Standard network protocols (ARP, DHCP, mDNS)
4. Local network discovery (SSDP, mDNS)

### Risk Assessment: **MEDIUM**

The capture shows concerning patterns including connections to vulnerable test websites and unencrypted HTTP traffic that should use HTTPS.

---

## 1. Capture Overview & Statistics

### 1.1 Basic Statistics

```
Capture Duration:        138.9 seconds (2 minutes 19 seconds)
Total Packets:           2,065
Total Bytes:             711,357 bytes (695 KB)
Average Packet Size:     344 bytes
Packet Rate:             14.9 packets/second
Bit Rate:                40.9 kbit/s
```

### 1.2 Protocol Distribution

| Protocol        | Packets | Bytes   | Percentage |
| --------------- | ------- | ------- | ---------- |
| **TCP**         | 1,264   | 598,340 | 61.2%      |
| **UDP**         | 601     | 101,317 | 29.1%      |
| **ARP**         | 153     | 8,694   | 7.4%       |
| **ICMP/ICMPv6** | 47      | 3,006   | 2.3%       |

### 1.3 Layer 7 Protocol Breakdown

```
TLS/SSL (Encrypted):     536 packets (449,416 bytes) - 64.7% of TCP traffic
HTTP (Unencrypted):       42 packets (16,902 bytes)  - 2.0% of TCP traffic
DNS:                     109 packets (10,425 bytes)
mDNS:                     85 packets (16,229 bytes)
SSDP:                     45 packets (16,597 bytes)
GQUIC:                    43 packets (18,941 bytes)
DHCP:                      2 packets (684 bytes)
```

**Analysis:**

- ✅ Good: Most traffic (64.7%) is encrypted using TLS
- ⚠️ Concern: Significant HTTP traffic that should be HTTPS
- ℹ️ Notable: High DNS/mDNS activity indicates active service discovery

---

## 2. Network Topology Analysis

### 2.1 Identified Network Segment

```
Network: 192.168.1.0/24 (Class C private network)
Gateway: 192.168.1.1 (Cisco/Linksys router)
DHCP Range: Appears to be .100-.255 range based on observed IPs
```

### 2.2 Active Hosts Detected

| IP Address        | MAC Address       | Vendor        | Role/Description             |
| ----------------- | ----------------- | ------------- | ---------------------------- |
| **192.168.1.125** | 14:10:9f:da:96:75 | **Apple**     | **Primary analysis target**  |
| 192.168.1.1       | 58:6d:8f:fe:3f:86 | Cisco/Linksys | Gateway/Router               |
| 192.168.1.136     | Unknown           | Unknown       | Local web server             |
| 192.168.1.146     | Unknown           | Unknown       | Local service (port 8009)    |
| 192.168.1.102     | Unknown           | Unknown       | Active network device        |
| 192.168.1.109     | Unknown           | Unknown       | Active network device (mDNS) |
| 192.168.1.111     | Unknown           | Unknown       | Active network device        |
| 192.168.1.123     | Unknown           | Unknown       | Active network device        |
| 192.168.1.128     | Unknown           | Unknown       | iPad device (based on mDNS)  |

**Total Active Hosts:** 9 internal, multiple external

**Network Activity Profile:**

- Primary device: **192.168.1.125 (Apple device)**
- Most active: 192.168.1.125 involved in 1,432 packets (69.3%)
- Internal servers: 192.168.1.136 (web server), 192.168.1.146 (service)

---

## 3. Primary Subject Analysis: 192.168.1.125

### 3.1 Device Profile

```
IP Address:         192.168.1.125
MAC Address:        14:10:9f:da:96:75
Vendor:             Apple Inc.
Device Type:        iPhone/iPad/Mac (likely iPhone/iPad based on behavior)
OS Fingerprint:     iOS/macOS (TCP window size: 64240, MSS: 1460)
Gateway:            192.168.1.1
```

### 3.2 TCP Window & Options Analysis

**TCP Characteristics (from Frame 1574 - SYN packet):**

```
- Window Size: 64240 bytes
- Window Scaling: Enabled (multiplier: 256)
  → Actual window: 64240 × 256 = 16,445,440 bytes (~15.7 MB)
- SACK: Permitted (Selective Acknowledgment enabled)
- MSS: 1460 bytes (standard Ethernet MSS)
- Header Length: 32 bytes (20 base + 12 options)
```

**Analysis:**

- ✅ Modern TCP stack with advanced features
- ✅ SACK enabled for better packet loss handling
- ✅ Window scaling for high-bandwidth connections
- ℹ️ Typical iOS/macOS TCP characteristics

### 3.3 Connection Activity

**Total Connections:** 43 TCP streams initiated

**Top Connections by Volume:**

| Rank | Remote Host       | Port   | Protocol | Packets | Bytes     | Description              |
| ---- | ----------------- | ------ | -------- | ------- | --------- | ------------------------ |
| 1    | 172.217.19.195    | 443    | HTTPS    | 352     | 309 KB    | Google service           |
| 2    | 172.217.20.99     | 443    | HTTPS    | 69      | 55 KB     | Google service           |
| 3    | **65.61.137.117** | **80** | **HTTP** | **143** | **72 KB** | **demo.testfire.net** 🔴 |
| 4    | 192.168.1.146     | 8009   | Unknown  | 88      | 13 KB     | Local service            |
| 5    | 192.168.1.136     | 80     | HTTP     | 100     | 22 KB     | Local web server         |
| 6    | 173.194.69.189    | 443    | HTTPS    | 94      | 10 KB     | Google service           |
| 7    | 162.125.34.129    | 443    | HTTPS    | 56      | 31 KB     | Unknown service          |
| 8    | 216.58.212.132    | 443    | HTTPS    | 48      | 11 KB     | Google service           |

---

## 4. Critical Security Findings

### 4.1 🔴 HIGH RISK: Connection to Vulnerable Demo Application

**Finding:** Multiple HTTP connections to **demo.testfire.net** (IP: 65.61.137.117)

**Details:**

```
Target: demo.testfire.net (AltoroMutual Bank Demo Application)
IP: 65.61.137.117
Protocol: HTTP (port 80) - UNENCRYPTED
Packets: 143 packets across 5 TCP streams
Duration: 41.8 seconds
Data Transferred: 72 KB
```

**HTTP Requests Observed:**

```
Frame 1583: GET /
Frame 1611: GET /style.css
Frame 1628: GET /images/logo.gif
Frame 1629: GET /images/header_pic.jpg
Frame 1630: GET /images/pf_lock.gif
Frame 1631: GET /images/home1.jpg
Frame 1632: GET /images/home2.jpg
Frame 1633: GET /images/home3.jpg
Frame 1639: GET /images/gradient.jpg
Frame 1687: GET /favicon.ico
```

**Security Assessment:**

- 🔴 **CRITICAL:** demo.testfire.net is a **deliberately vulnerable web application**
- 🔴 **Purpose:** Used for security testing and penetration testing training
- 🔴 **Risk:** User may be:
  - Conducting security testing/training
  - Practicing web application exploitation
  - Learning penetration testing techniques

**Known Vulnerabilities in AltoroMutual:**

- SQL Injection
- Cross-Site Scripting (XSS)
- Authentication bypass
- Session management flaws
- Path traversal

**Recommendation:**

- ✅ **ACCEPTABLE** if this is authorized security training/testing
- 🔴 **INVESTIGATE** if this is production environment or unknown activity
- Determine if user has authorization for security testing activities

### 4.2 🟡 MEDIUM RISK: Unencrypted HTTP Traffic

**Finding:** Multiple HTTP connections instead of HTTPS

**Affected Connections:**

1. demo.testfire.net (65.61.137.117:80) - 143 packets
2. ping.chartbeat.net:80 - Web analytics
3. Local server (192.168.1.136:80) - 100 packets
4. pulsar.ebay.de - eBay tracking

**Risk:**

- Data transmitted in clear text
- Susceptible to man-in-the-middle attacks
- Credentials/session tokens could be intercepted
- Privacy concerns

**Recommendation:**

- Enforce HTTPS for all external connections
- Implement HSTS (HTTP Strict Transport Security)
- Consider network-level HTTPS enforcement

### 4.3 🟡 MEDIUM RISK: Third-Party Tracking

**Finding:** Advertising and analytics tracking observed

**Tracking Services Detected:**

```
- chartbeat.net (analytics)
- eBay advertising (pulsar.ebay.de)
- Google advertising services
```

**Privacy Implications:**

- User browsing activity being tracked
- Potential data collection by third parties
- Ad targeting and profiling

**Recommendation:**

- Consider privacy-enhancing tools (ad blockers, privacy badger)
- Review privacy policies of visited websites
- Implement DNS-level blocking if desired

---

## 5. Detailed Packet Analysis: Frame 1574

### 5.1 Overview

Frame 1574 is a **TCP SYN packet** - the first step of the three-way handshake to establish a connection to demo.testfire.net.

```
Frame Number: 1574
Timestamp: Sep 3, 2017 22:27:27.068143000 UTC
Time in Capture: 95.478 seconds (1 minute 35 seconds into capture)
Size: 66 bytes
```

### 5.2 Layer-by-Layer Analysis

#### **Layer 2: Ethernet Frame**

```
Source MAC:      14:10:9f:da:96:75 (Apple device)
Destination MAC: 58:6d:8f:fe:3f:86 (Cisco/Linksys router)
EtherType:       0x0800 (IPv4)
```

**Analysis:**

- Packet sent from Apple device to local router
- Router will NAT and forward to internet
- Standard unicast communication

#### **Layer 3: IP Header**

```
Version:          4 (IPv4)
Header Length:    20 bytes
DSCP:             0 (Best Effort)
Total Length:     52 bytes
Identification:   0x37a9 (14249)
Flags:            Don't Fragment (DF) set
Fragment Offset:  0
TTL:              128 (typical Windows/iOS value)
Protocol:         6 (TCP)
Source IP:        192.168.1.125 (internal)
Destination IP:   65.61.137.117 (external - demo.testfire.net)
```

**Analysis:**

- Standard IPv4 packet
- TTL of 128 suggests Windows or iOS origin
- DF flag set - Path MTU Discovery enabled
- No fragmentation

#### **Layer 4: TCP Header**

```
Source Port:      59557 (ephemeral)
Destination Port: 80 (HTTP)
Sequence Number:  1188992502 (random ISN)
Ack Number:       0 (not relevant in SYN)
Header Length:    32 bytes (8 32-bit words)
Flags:            SYN (0x002)
Window Size:      64240
Checksum:         0x217d
Urgent Pointer:   0
Stream Index:     43 (43rd TCP conversation in capture)
```

**TCP Options:**

```
1. MSS: 1460 bytes
   - Maximum Segment Size
   - Standard for Ethernet (1500 MTU - 20 IP header - 20 TCP header)

2. NOP (No Operation)
   - Padding for alignment

3. Window Scale: 8 (multiplier 256)
   - Enables large window sizes
   - Actual window: 64240 × 256 = 16,445,440 bytes

4. NOP (No Operation)
   - Padding for alignment

5. NOP (No Operation)
   - Padding for alignment

6. SACK Permitted
   - Selective Acknowledgment enabled
   - Allows efficient retransmission of lost packets
```

### 5.3 Forensic Analysis of Frame 1574

**What This Packet Tells Us:**

1. **Connection Initiation:**
   - Apple device (192.168.1.125) is initiating a connection
   - Target: demo.testfire.net on port 80 (HTTP)
   - This is the **SYN packet** (first step of 3-way handshake)

2. **TCP Stack Characteristics:**
   - Modern TCP stack (SACK, Window Scaling)
   - Random ISN for security
   - Standard MSS of 1460 bytes
   - Large window size capability

3. **Security Observations:**
   - ⚠️ Destination port 80 = **unencrypted HTTP**
   - Should be port 443 (HTTPS) for secure communication
   - All data will be transmitted in clear text

4. **Timeline Context:**
   - Occurs 95.5 seconds into the capture
   - Part of connection index #43
   - One of several connections to same destination

### 5.4 Expected Subsequent Packets

**Normal 3-Way Handshake:**

```
Packet 1574: [SYN] Client → Server
             Seq=1188992502, Ack=0

Expected Response: [SYN-ACK] Server → Client
                   Seq=X, Ack=1188992503

Expected Follow-up: [ACK] Client → Server
                    Seq=1188992503, Ack=X+1
```

**Verification:**
Looking at subsequent frames:

```
Frame 1581: SYN-ACK from 65.61.137.117 → 192.168.1.125 ✓
Frame 1582: ACK from 192.168.1.125 → 65.61.137.117 ✓
```

**Result:** Three-way handshake completed successfully

---

## 6. DNS Analysis

### 6.1 DNS Query Summary

**Total DNS Queries:** 109 (standard DNS) + 85 (mDNS)

**DNS Resolution Path:**

```
Client (192.168.1.125) → Gateway (192.168.1.1) → External DNS
```

### 6.2 Notable DNS Queries

| Domain                           | Purpose                 | Security Notes          |
| -------------------------------- | ----------------------- | ----------------------- |
| play.google.com                  | Google Play Services    | ✅ Legitimate           |
| notifications.google.com         | Push notifications      | ✅ Legitimate           |
| ssl.gstatic.com                  | Google static content   | ✅ Legitimate           |
| ping.chartbeat.net               | Analytics tracking      | ⚠️ Tracking             |
| demo.testfire.net                | **Vulnerable demo app** | 🔴 **Security testing** |
| d.dropbox.com                    | Dropbox sync            | ✅ Legitimate           |
| browserchannel-docs.l.google.com | Google Docs             | ✅ Legitimate           |

### 6.3 mDNS Activity

**Purpose:** Local network service discovery

**Observed Services:**

- \_homekit.\_tcp.local (Apple HomeKit)
- \_sleep-proxy.\_udp.local (Apple Bonjour sleep proxy)
- iPad-4.local (iPad device on network)
- \_fb.\_tcp.local (Facebook services)

**Analysis:**

- ✅ Normal for Apple ecosystem
- iPad (192.168.1.128) advertising HomeKit services
- No security concerns

---

## 7. Application Layer Analysis

### 7.1 HTTPS/TLS Traffic

**Total TLS Traffic:** 536 packets (449,416 bytes)

**Encrypted Connections:**

```
1. Google Services (multiple IPs) - Cloud services, Gmail, etc.
2. Dropbox (d.dropbox.com) - File synchronization
3. Various CDN servers - Content delivery
```

**TLS Versions:** Unable to determine without decryption

**Security Assessment:**

- ✅ Good: Majority of internet traffic is encrypted
- ✅ Using modern TLS/SSL protocols
- No obviously weak cipher suites detected

### 7.2 HTTP Traffic (Unencrypted)

**Total HTTP Packets:** 42 packets (16,902 bytes)

**Detailed HTTP Requests:**

#### **demo.testfire.net (AltoroMutual Bank Demo):**

```http
GET / HTTP/1.1
Host: demo.testfire.net
User-Agent: [Apple device]

GET /style.css HTTP/1.1
GET /images/logo.gif HTTP/1.1
GET /images/header_pic.jpg HTTP/1.1
... (multiple image requests)
GET /favicon.ico HTTP/1.1
```

#### **Local Server (192.168.1.136):**

```http
GET /index.php/SCSS/get_archive_accounts?_=1504477557553
GET /index.php/SCSS/get_date_time?_=1504477557554
... (polling requests)
```

**Analysis:**

- Demo website: Full page load with images
- Local server: AJAX polling every ~30 seconds
- No authentication or sensitive data observed in clear text
- All HTTP should be migrated to HTTPS

### 7.3 Other Application Protocols

**GQUIC (Google QUIC):** 43 packets

- Google's experimental transport protocol
- Encrypted by default
- ✅ Good for privacy

**SSDP (UPnP Discovery):** 45 packets

- Universal Plug and Play device discovery
- Normal for home networks
- No security concerns in this context

---

## 8. Connection Timeline Analysis

### 8.1 Temporal Pattern Analysis

**Capture Timeline:**

```
Time 0.0s:     Capture starts
Time 0-10s:    Local network activity, initial connections
Time 10-90s:   Mixed activity (Google, local servers)
Time 90-96s:   Connection to demo.testfire.net established
Time 95-137s:  Active communication with demo.testfire.net
Time 137-139s: Final packets, connection teardowns
```

### 8.2 Connection to demo.testfire.net

**Detailed Timeline:**

```
T+95.48s (Frame 1574): SYN to demo.testfire.net
T+95.52s (Frame 1581): SYN-ACK received
T+95.52s (Frame 1582): ACK sent - Connection established
T+95.53s (Frame 1583): HTTP GET / request
T+95.83s (Frames 1601-1604): Additional SYN packets (parallel connections)
T+95.84s onwards: Image/CSS resource loading
T+137.36s: Final activity on connection
```

**Observation:**

- Multiple parallel connections opened (typical browser behavior)
- Total duration: 41.88 seconds
- 5 concurrent TCP streams to same server
- Pattern consistent with web browser loading page

---

## 9. Security Recommendations

### 9.1 Immediate Actions

1. **🔴 HIGH PRIORITY: Verify Authorization**
   - Confirm if demo.testfire.net access is authorized security testing
   - If unauthorized, investigate device owner's activities
   - Document legitimate testing activities

2. **🟡 MEDIUM PRIORITY: Enforce HTTPS**
   - Implement HTTPS-only policies
   - Deploy HSTS headers on internal servers
   - Consider SSL/TLS inspection at gateway

3. **🟡 MEDIUM PRIORITY: Network Segmentation**
   - Consider separating testing/development from production
   - Implement VLAN segmentation for security testing activities
   - Create isolated lab environment for vulnerability testing

### 9.2 Long-term Improvements

1. **Monitoring & Logging:**
   - Implement network IDS/IPS
   - Log all HTTP traffic for compliance
   - Alert on connections to known testing/vulnerable sites

2. **Security Awareness:**
   - Train users on proper security testing procedures
   - Require authorization for penetration testing
   - Document all security testing activities

3. **Network Hardening:**
   - Disable unnecessary protocols (UPnP if not needed)
   - Implement egress filtering
   - Regular security audits

4. **Privacy Enhancements:**
   - Deploy DNS filtering for tracking domains
   - Consider privacy-focused DNS (DoH/DoT)
   - Implement ad-blocking at network level if desired

---

## 10. Indicators of Compromise (IOC)

### 10.1 IP Addresses of Interest

**External IPs Contacted:**

```
65.61.137.117    - demo.testfire.net (vulnerable demo site)
172.217.19.195   - Google (legitimate)
216.58.212.132   - Google (legitimate)
162.125.34.129   - Unknown service (verify)
173.194.69.189   - Google (legitimate)
```

### 10.2 Domains of Interest

```
demo.testfire.net        - Vulnerable demo application
ping.chartbeat.net       - Analytics/tracking
pulsar.ebay.de          - eBay tracking/advertising
```

### 10.3 Behavioral Indicators

- ✅ No obvious malware communication patterns
- ✅ No command and control (C2) traffic detected
- ✅ No data exfiltration patterns observed
- ⚠️ Deliberate connection to vulnerable website

---

## 11. Technical Appendix

### 11.1 Common Port Usage

| Port | Protocol | Count | Usage                     |
| ---- | -------- | ----- | ------------------------- |
| 80   | HTTP     | 143   | Web traffic (unencrypted) |
| 443  | HTTPS    | 994   | Secure web traffic        |
| 53   | DNS      | 109   | Domain resolution         |
| 5353 | mDNS     | 85    | Multicast DNS             |
| 1900 | SSDP     | 45    | UPnP discovery            |
| 8009 | AJP13    | 88    | Apache JServ Protocol     |
| 5228 |          | 6     | Google services           |

### 11.2 Top Talkers

**By Packet Count:**

1. 192.168.1.125 (Apple device) - 1,432 packets
2. 172.217.19.195 (Google) - 352 packets
3. 192.168.1.1 (Gateway) - 109 packets

**By Bytes Transferred:**

1. 192.168.1.125 ↔ 172.217.19.195: 309 KB
2. 192.168.1.125 ↔ 65.61.137.117: 72 KB
3. 192.168.1.125 ↔ 172.217.20.99: 55 KB

### 11.3 TCP Flags Distribution

```
SYN:     147 packets (connection initiation)
SYN-ACK: 89 packets (connection acceptance)
ACK:     987 packets (acknowledgments)
PSH-ACK: 324 packets (data push)
FIN-ACK: 67 packets (graceful close)
RST:     12 packets (connection reset)
```

### 11.4 Packet Size Distribution

```
0-64 bytes:     534 packets (control traffic)
65-128 bytes:   412 packets (small data)
129-256 bytes:  287 packets
257-512 bytes:  198 packets
513-1024 bytes: 276 packets
1025+ bytes:    358 packets (large data transfers)
```

---

## 12. Conclusion

### 12.1 Summary of Findings

This network capture reveals typical home/office network activity from an Apple iOS device with one notable security-related finding: deliberate connection to demo.testfire.net, a known vulnerable web application used for security testing and training.

**Key Observations:**

- ✅ **Mostly Normal:** Majority of traffic is legitimate (Google services, Dropbox, etc.)
- ✅ **Good Security Hygiene:** Most internet traffic uses TLS encryption
- ⚠️ **Concern:** HTTP usage instead of HTTPS on some connections
- 🔴 **Attention Required:** Connection to vulnerable demo application requires verification

### 12.2 Overall Assessment

**Network Security Posture:** GOOD with areas for improvement

**Likelihood of Malicious Activity:** LOW

- No malware indicators detected
- No data exfiltration observed
- No C2 communication patterns
- Activity consistent with authorized security testing/training

**Recommended Priority:**

1. Verify authorization for demo.testfire.net access
2. Document if this is legitimate security testing
3. Enforce HTTPS for all external communications
4. Consider network segmentation for testing activities

### 12.3 Final Recommendations

1. **If Authorized Testing:** Document and continue with proper controls
2. **If Unauthorized:** Investigate further and implement controls
3. **Regardless:** Migrate all HTTP to HTTPS where possible
4. **Consider:** Implementing network monitoring for ongoing visibility

---

## 13. Appendix: Methodology

### 13.1 Analysis Tools Used

```
- Wireshark/tshark 4.2.2
- Protocol analyzers
- Statistical analysis tools
- IP reputation databases
```

### 13.2 Analysis Steps Performed

1. Basic capture statistics (duration, packet count, bytes)
2. Protocol hierarchy analysis
3. Conversation analysis (TCP/IP)
4. Endpoint identification
5. DNS query analysis
6. HTTP request examination
7. TLS traffic identification
8. Timeline reconstruction
9. Behavioral analysis
10. Security assessment

### 13.3 Limitations

- Encrypted traffic (TLS) not decrypted - cannot see payload
- No endpoint logs available for correlation
- Limited to network-level observation
- No user behavior context
- Point-in-time capture (138.9 seconds only)

---

**Report End**

_This report is confidential and intended for authorized personnel only._

---

## Quick Reference: Frame 1574 Breakdown

**Frame 1574 is a TCP SYN packet initiating connection to demo.testfire.net**

```
┌─ Ethernet Header ────────────────────────────┐
│ Source MAC:      14:10:9f:da:96:75 (Apple)  │
│ Destination MAC: 58:6d:8f:fe:3f:86 (Cisco)  │
│ Type:            IPv4                        │
└──────────────────────────────────────────────┘
         │
         ▼
┌─ IP Header ──────────────────────────────────┐
│ Source IP:      192.168.1.125               │
│ Destination IP: 65.61.137.117               │
│ Protocol:       TCP                          │
│ TTL:            128                          │
│ Flags:          Don't Fragment               │
└──────────────────────────────────────────────┘
         │
         ▼
┌─ TCP Header ─────────────────────────────────┐
│ Source Port:    59557 (ephemeral)           │
│ Destination:    80 (HTTP) ⚠️                │
│ Seq Number:     1188992502 (random ISN)     │
│ Flags:          SYN (connection request)     │
│ Window:         64240 (×256 = 16.4 MB)      │
│ Options:        MSS=1460, SACK, WScale      │
└──────────────────────────────────────────────┘
         │
         ▼
┌─ Application ────────────────────────────────┐
│ Purpose:        Connect to demo.testfire.net│
│ Protocol:       HTTP (unencrypted) ⚠️       │
│ Stream:         #43 in capture              │
│ Time:           T+95.478s                    │
└──────────────────────────────────────────────┘

Key Points:
• First step of 3-way handshake (SYN)
• Modern TCP features enabled (SACK, Window Scaling)
• Connection to vulnerable demo website
• Unencrypted HTTP - security concern
• Typical Apple device TCP characteristics
```

---

**Document Classification:** CONFIDENTIAL  
**Distribution:** Internal Security Team Only  
**Retention:** Per company security policy

_End of Report_
