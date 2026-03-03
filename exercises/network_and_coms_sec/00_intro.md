# Exercises Intro

## [INTRO.01] Wireshark Revisited

Download `intro01.zip` from Fronter. Use `tcp.analysis.*` filters and the I/O graph.

**In `ncs01.pcapng`:**
- Locate a **fast retransmit** packet — what is it?
### Fast Retransmit
A fast retransmit occurs when the sender retransmits a segment before its retransmission timer expires. This is triggered by receiving 3 duplicate ACKs, which signals that a specific segment was lost. Instead of waiting for the timeout, the sender immediately resends the missing segment.
tcp.analysis.fast_retransmission

- Find **spurious retransmission** packets — what are they?
### Spurious Retransmission
A spurious retransmission is when a segment is retransmitted even though it had already been successfully acknowledged by the receiver. This happens when the sender retransmits due to a delayed or lost ACK, even though the original segment arrived fine — meaning the retransmission was unnecessary.
tcp.analysis.spurious_retransmission

- Find **out-of-order** packets — why does this happen?
### Out-of-Order Packets
Out-of-order packets occur when segments arrive at the receiver in a different order than they were sent. This happens due to network congestion causing different packets to take different paths with varying delays, or because an earlier segment was lost and a later one arrived first.
tcp.analysis.out_of_order

- How does Wireshark identify a **lost segment**? Find the filter.
### Lost Segment
Wireshark identifies a lost segment when there is a gap in the sequence numbers — meaning an expected sequence number is skipped entirely. This is detected by observing that the next received segment has a sequence number higher than expected, indicating one or more segments never arrived.
tcp.analysis.lost_segment

- Find **duplicate ACKs** — why do they occur?
### Duplicate ACKs
Duplicate ACKs occur when the receiver gets an out-of-order segment and re-sends an ACK for the last correctly received in-order segment. Each additional out-of-order or missing segment causes another duplicate ACK to be sent, signaling to the sender that a gap exists in the received data.
tcp.analysis.duplicate_ack

**In `ncs02.pcapng`:**
- Find packets where the **window size changes** — why?

### Window Size Changes
The TCP window size is controlled by the receiver and represents how much data it is willing to accept at a time (receive buffer space). The window size changes dynamically as part of flow control: if the receiver's buffer is filling up (ex. the application isn't reading data fast enough), it shrinks the advertised window to slow the sender down.
When buffer space frees up again, it increases the window to allow more data through.
A window size of 0 means the receiver is telling the sender to stop transmitting entirely until further notice.
tcp.analysis.window_update — flags packets where the receiver announces a changed window size
tcp.analysis.zero_window — flags when the window hits 0


---

## [INTRO.02] Describe a Protocol
In study groups: find the **RFC number** and describe the **header** for each:

`HTTP` · `FTP` · `SMTP` · `DNS` · `SNMP` · `TCP` · `UDP` · `ICMP` · `IP` · `ARP` · `802.3` · `802.11x` · `QUIC`


### HTTP — RFC 9110
Text-based protocol. No fixed binary header — requests contain a method (GET/POST etc.), URI, HTTP version, and headers (Host, Content-Type, etc.). Responses contain a status code (200, 404 etc.) and headers. Body is optional.

### FTP — RFC 959
Uses two TCP connections: port 21 for control (commands like USER, PASS, RETR) and port 20 for data transfer. Commands and responses are plain text. No single binary header structure.

### SMTP — RFC 5321
Text-based, port 25. Commands include EHLO, MAIL FROM, RCPT TO, DATA. No binary header — the message itself has headers (From, To, Subject) defined by RFC 5322. Used only for sending mail, not receiving.

### DNS — RFC 1035
Binary header (12 bytes): Transaction ID, Flags (QR, Opcode, AA, TC, RD, RA), Question Count, Answer Count, Authority Count, Additional Count. Followed by variable-length question and answer sections. Uses port 53, UDP (or TCP for large responses).

### SNMP — RFC 1157
Used for network device monitoring. Fields: Version, Community string (acts as a password), PDU Type (GET, SET, TRAP etc.), Request ID, Error Status, Error Index, Variable Bindings (OID-value pairs). Uses port 161 (UDP).

### TCP — RFC 9293
Binary header (min 20 bytes): Source Port, Destination Port, Sequence Number, Acknowledgment Number, Data Offset, Flags (SYN, ACK, FIN, RST, PSH, URG), Window Size, Checksum, Urgent Pointer, optional Options. Connection-oriented, reliable, ordered delivery.

### UDP — RFC 768
Minimal 8-byte header: Source Port, Destination Port, Length, Checksum. No connection setup, no reliability, no ordering. Fast and lightweight — used for DNS, streaming, gaming.

### ICMP — RFC 792
Used for network diagnostics (ping, traceroute). Header: Type (8=echo request, 0=echo reply), Code (subtype), Checksum, Rest of Header (varies by type, e.g. Identifier + Sequence Number for ping). Operates at Layer 3, carried inside IP packets.

### IP (IPv4) — RFC 791
Binary header (min 20 bytes): Version, IHL, DSCP/TOS, Total Length, Identification, Flags (DF, MF), Fragment Offset, TTL, Protocol (6=TCP, 17=UDP), Header Checksum, Source IP, Destination IP, optional Options.

### ARP — RFC 826
Resolves IP addresses to MAC addresses on a local network. Fields: Hardware Type, Protocol Type, Hardware Address Length, Protocol Address Length, Operation (1=request, 2=reply), Sender MAC, Sender IP, Target MAC, Target IP. Layer 2, never routed.

### 802.3 (Ethernet) — IEEE standard
Layer 2 frame: Preamble (7 bytes), SFD (1 byte), Destination MAC (6 bytes), Source MAC (6 bytes), EtherType/Length (2 bytes), Payload (46–1500 bytes), FCS/CRC (4 bytes). EtherType identifies the Layer 3 protocol (0x0800 = IPv4, 0x0806 = ARP).

### 802.11 (Wi-Fi) — IEEE standard
Wireless LAN frame. Header includes: Frame Control (type, subtype, flags), Duration/ID, Address 1–4 (up to 4 MAC addresses for source, destination, BSSID, transmitter), Sequence Control, optional QoS Control, Payload, FCS. More complex than Ethernet due to wireless management needs (authentication, association frames etc.).

### QUIC — RFC 9000
Modern transport protocol built on UDP, developed by Google. Combines features of TCP + TLS into one layer. Header contains: Header Form (long/short), Version, Connection ID (persists across network changes), Packet Number, Payload (always encrypted). Designed for low-latency HTTP/3 connections — eliminates TCP handshake overhead.