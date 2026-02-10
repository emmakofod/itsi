# Transport Layer - Complete Notes

## Overview

The transport layer sits between the application and network layers in the network stack. Two main protocols: **TCP** and **UDP**

---

## Processes Communicating

**Process** = program running within a host

- **Within same host**: Two processes communicate using inter-process communication (defined by OS)
- **Different hosts**: Processes communicate by exchanging messages
- **Key question**: When creating a new network app, do we use UDP or TCP?

---

## Sockets

**Socket** = interface between application and transport layer (analogous to a door)

- Process sends/receives messages to/from its socket
- Sending process "shoves" message out the door
- Relies on transport infrastructure to deliver message to receiving socket

### Addressing Processes

To receive messages, a process must have **identifiers**:

- **IP address** - identifies the host
- **Port number** - identifies the specific process on that host

### Two Socket Types for Two Transport Services:

- **UDP**: unreliable datagram
- **TCP**: reliable, byte stream-oriented

---

## Multiplexing/Demultiplexing

### Key Concept

- **Multiplexing** (at sender): Handle data from multiple sockets, add transport header (used later for demultiplexing)
- **Demultiplexing** (at receiver): Use header info to deliver received segments to correct socket

### How Demultiplexing Works:

1. Host receives IP datagrams
   - Each datagram has source IP address and destination IP address
   - Each datagram carries one transport-layer segment
   - Each segment has source and destination port number
2. Host uses **IP addresses & port numbers** to direct segment to appropriate socket

### Four Elements to Identify a Connection:

1. Source IP address
2. Source port number
3. Destination IP address
4. Destination port number

**Note**: A process can have one or more sockets

---

## TCP (Transmission Control Protocol)

### TCP Characteristics

**Connection-oriented service**:

- Client and server exchange transport layer information before messages flow (**handshaking**)
- **Full duplex connection**: both processes can send messages to each other
- **Point-to-point**: one sender, one receiver
- Connection required before sending data

**Reliable data transfer service**:

- All data sent **without error** and **in order**
- No missing or duplicate bytes
- TCP is **reliable** - all data is sent, no loss

**Flow and Congestion Control**:

- **Flow control**: Ensures no overloading of receiver
- **Congestion control**: Sender decides how many packets to send based on errors received
  - Sender will not overwhelm receiver

**Security**:

- TCP is **NOT secure** by default
- Use **TLS (SSL)** to enhance TCP security from the application layer

**Summary**: TCP provides **reliable, in-order byte-stream transfer ("pipe")** between client and server

---

### TCP Connection Establishment

**Client must contact server**:

- Server process must be running first
- Server must have created a socket that waits for client's contact

**Client contacts server by**:

1. Creating TCP socket
2. Specifying IP address and port number of server process
3. When client creates socket: client TCP establishes connection to server TCP

**Server response**:

- When contacted by client, server TCP creates **new socket** to communicate with that particular client
- Allows server to talk with **multiple clients**
- **Source port numbers** used to distinguish clients

---

### TCP Three-Way Handshake

**Process** (ladder diagram format):

```
Client (Alice)                    Server (Bob)
      |                                |
      |--------SYN (seq=x)------------>|  1. Client sends SYN
      |                                |
      |<---SYN-ACK (seq=y, ack=x+1)---|  2. Server responds with SYN-ACK
      |                                |
      |--------ACK (ack=y+1)---------->|  3. Client sends ACK
      |                                |
   Connection Established
```

**Steps**:

1. **Alice sends Bob** a "synchronize" (**SYN**) message with its own sequence number **x**
2. **Bob replies** with synchronize-acknowledgment (**SYN-ACK**) message with its own sequence number **y** and ack number **x+1**
3. **Alice replies** with **ACK** message with ack number **y+1**. Bob doesn't need to reply to this.

**Important**: SYN is only used to connect, not after. Connection is now established.

---

### TCP Segment Structure

**32 bits wide** (representation width, NOT header size)

- Minimum header size: **20 bytes** = 5 d-words (double words) = 5 lines

#### Header Fields (in order):

1. **Source port** (16 bits)
   - Sender's port number
   - Max: 2^16 = 0 to ~65,535 (some reserved)
   - OS tries to find first available port, usually higher numbers

2. **Destination port** (16 bits)
   - The port you wish to connect to
   - The service/process you want (e.g., 80 for HTTP, 25 for SMTP)

3. **Sequence number** (32 bits)
   - Random number between 0 and ~4 billion (2^32)
   - Byte stream "number" of first byte in segment's data
   - Used to track position in communication
   - Ensures packets are put in right order

4. **Acknowledgment number** (32 bits)
   - Sequence number of next byte expected from other side
   - Server acknowledges client's number and gives related response
   - **NOT** SYN nor ACK flag
   - By default: **Cumulative ACK** (acknowledges all bytes up to this number)
   - With SACK option: Can also use **Selective ACK** (see SACK section below)

5. **Header length** (4 bits)
   - Can vary
   - Minimum: 20 bytes = 5 d-words = 5 lines
   - Indicates number of 32-bit words in header

6. **Not used** (6 bits)
   - Reserved, not used in TCP

7. **Flags** (6 bits):
   - **S (SYN)**: Synchronize - only used to establish connection
   - **A (ACK)**: Acknowledge - indicates acknowledgment is valid
   - **F (FIN)**: Finish - only used to close connection gracefully
   - **R (RST)**: Reset - ungraceful teardown, brute closing
     - Used for unrecoverable errors, state errors
   - **U (URG)**: Urgent - urgent data pointer is valid
   - **P (PSH)**: Push - used for segmentation
     - When data too big for one packet, split into multiple
     - Last packet gets P flag to say "this is one complete thing"
     - Used in protocols like Telnet

8. **Receive window** (16 bits) - **FLOW CONTROL**
   - Indicates how many packets receiver can and wants to receive
   - "I cannot and will not receive more than this until I've acknowledged data first"
   - Cannot be bigger than 2^16
   - Number of bytes receiver is willing to accept

9. **Checksum** (16 bits)
   - Simple calculation to detect errors in packet
   - Not bulletproof - calculation is too basic
   - Internet checksum (as in UDP)

10. **Urgent data pointer** (16 bits)
    - Not used a lot
    - Points to urgent data (when URG flag set)

11. **Options** (variable length)
    - Variable length field
    - Can specify additional parameters

12. **Application data (payload)** (variable length)
    - The actual data being transmitted

---

### TCP Maximum Segment Size (MSS)

**The Magic Number: 1500 bytes (MTU - Maximum Transmission Unit)**

The calculation:

```
MTU (Maximum Transmission Unit)     = 1500 bytes
- IP header                         =   20 bytes
- TCP header                        =   20 bytes
_________________________________________________
= MSS (Maximum Segment Size)        = 1460 bytes
```

**Key points**:

- **MTU (1500 bytes)**: Maximum size of a packet that can be transmitted over Ethernet
- **IP header (20 bytes)**: Network layer header
- **TCP header (20 bytes)**: Transport layer header minimum size
- **MSS (1460 bytes)**: Maximum amount of actual data that can fit in one TCP segment

This is why TCP typically segments data into chunks of 1460 bytes or less - it's the largest payload that fits within the standard Ethernet MTU when accounting for both IP and TCP headers.

**Important**: If TCP or IP options are used, the headers can be larger than 20 bytes, which would reduce the MSS accordingly.

---

### TCP Reliability: Sequence Numbers and ACKs

**Sequence numbers**:

- Byte stream "number" of first byte in segment's data
- Counting by bytes of data (not segments!)

**Acknowledgements**:

- Seq # of next byte expected from other side
- **Cumulative ACK**: Acknowledges all data received up to a certain point
- **Selective ACK (SACK)**: Can also acknowledge non-contiguous blocks of data (see SACK section)

**Example scenario** (simple telnet):

```
Host A                           Host B
User types 'C'
Seq=42, ACK=79, data='C' ------->
                                 Host ACKs receipt of 'C',
                     <-------    echoes back 'C'
                                 Seq=79, ACK=43, data='C'
Host ACKs receipt
of echoed 'C'
Seq=43, ACK=80 ---------------->
```

---

### Reliable Data Transfer: Go-Back-N vs Selective Repeat

**Go-Back-N**:

- If packet N is lost, retransmit N and ALL subsequent packets
- Even if some subsequent packets were received correctly
- Simpler receiver logic (no buffering of out-of-order packets)

**Selective Repeat**:

- If packet N is lost, only retransmit packet N
- Receiver buffers out-of-order packets
- More efficient but more complex
- Records which packets arrived (ack3, ack4, ack5)
- Only resends missing packet (pkt2)

**TCP uses**: Primarily Go-Back-N with some selective repeat features (SACK options)

---

### SACK (Selective Acknowledgment)

**What is SACK?**

- An optional TCP feature that improves performance when packets are lost
- Allows receiver to inform sender about **all segments that have been received successfully**
- More efficient than standard cumulative ACKs

**How Standard TCP Works (without SACK)**:

- Uses **cumulative ACKs** only
- ACK number indicates "next byte expected"
- If packet 2 is lost but packets 3, 4, 5 arrive → receiver can only ACK up to packet 1
- Sender doesn't know if packets 3, 4, 5 were received
- May unnecessarily retransmit packets that were already received

**How SACK Works**:

- Receiver can say: "I'm still waiting for packet 2, BUT I already have packets 3, 4, and 5"
- Sender only retransmits packet 2 (the missing one)
- Saves bandwidth and time!

**Example Scenario**:

```
Sender sends: pkt0, pkt1, pkt2, pkt3, pkt4, pkt5
Packet 2 is lost ❌
Receiver gets: pkt0, pkt1, [missing], pkt3, pkt4, pkt5

WITHOUT SACK:
  Receiver sends: ACK 2 (still waiting for pkt2)
  Sender thinks: "Maybe pkt3, pkt4, pkt5 were also lost"
  Sender retransmits: pkt2, pkt3, pkt4, pkt5 (wasteful!)

WITH SACK:
  Receiver sends: ACK 2, SACK(3-6) ← "I have packets 3-6"
  Sender knows: "Only pkt2 is missing"
  Sender retransmits: pkt2 only (efficient!)
```

**SACK in TCP Header**:

- SACK information goes in the **Options field** (variable length)
- During handshake, both sides negotiate whether to use SACK
- SACK option specifies ranges of bytes that have been received

**Format**:

```
SACK blocks specify ranges:
SACK: Left Edge | Right Edge
      (start)   | (end)
```

**Benefits of SACK**:

1. ✅ Reduces unnecessary retransmissions
2. ✅ Improves throughput, especially on lossy networks
3. ✅ Sender knows exactly which segments to retransmit
4. ✅ Faster recovery from packet loss

**Key Points**:

- SACK is **optional** - both sender and receiver must support it
- Negotiated during TCP handshake (SYN/SYN-ACK)
- Modern TCP implementations typically support SACK
- More complex than standard TCP, but much more efficient

**Relation to Go-Back-N and Selective Repeat**:

- Standard TCP (without SACK) behaves like **Go-Back-N**
- TCP with SACK behaves more like **Selective Repeat**
- SACK allows TCP to combine reliability with efficiency

**Practical Note**:
The pcap files mentioned in the slides (SACK files) show real examples of SACK in action. You can see:

- How SACK blocks are transmitted
- Which packets are selectively acknowledged
- How sender responds to SACK information

---

## Real-World Example: ACK vs SACK in Action

### Understanding the Difference: A Practical Capture Analysis

Let's look at a **real packet capture** showing exactly how SACK works when packets are lost. This example comes from `SACK_example_.pcapng`.

### The Scenario: Packet Loss Detected

**What Happened:**
Server is sending data to client in 7-byte chunks. Everything is fine until... packets get lost!

### Frame-by-Frame Analysis

#### **Normal Operation (Before Packet Loss):**

```
Frame 18: Server → Client
  Seq: 50, Len: 7 bytes
  Data: Bytes 50-57

Frame 19: Client → Server
  ACK: 57 ← "I received up to byte 56, send me byte 57 next"

✅ Everything working normally!
```

#### **💥 Packet Loss Occurs:**

```
Frame 20: Server → Client
  Seq: 85, Len: 7 bytes  ← WAIT! What happened to bytes 57-84?
  Data: Bytes 85-92

🔴 PACKETS WITH SEQ 57-84 WERE LOST! (28 bytes missing)
```

The server sent packets with sequence numbers 57-84, but they **never arrived** at the client. The client only received the packet starting at byte 85.

---

### 🔑 Here's Where SACK Shines!

#### **Frame 21: Client's Response WITH SACK**

```
Client → Server:
  ACK Number: 57  ← "I'm STILL waiting for byte 57" (cumulative ACK)

  BUT ALSO includes in TCP Options:
  SACK: Left Edge = 85, Right Edge = 92 ← "BUT I have bytes 85-92!"

  Header Length: 32 bytes (8 d-words)
  ↳ Extra 12 bytes for SACK option
```

**What the client is saying:**

> "Hey server! I'm officially waiting for byte 57 (my ACK says 57), BUT before you retransmit EVERYTHING, you should know I already successfully received bytes 85-92. So you only need to send me bytes 57-84. Don't waste bandwidth re-sending 85-92!"

**SACK Option Structure:**

```
TCP Options: (12 bytes)
  - NOP (1 byte) - padding
  - NOP (1 byte) - padding
  - SACK (10 bytes):
      Kind: 5 (SACK)
      Length: 10
      Left Edge: 85  (relative sequence number)
      Right Edge: 92 (relative sequence number)
```

---

### 📊 Comparison: With SACK vs Without SACK

#### **WITHOUT SACK (Traditional TCP/Go-Back-N):**

```
Server receives: ACK 57

Server thinks:
"Client wants byte 57. I have no idea if the client
got any packets after that. Better retransmit EVERYTHING
from byte 57 onwards."

Server retransmits:
  - Bytes 57-64  ← Needed
  - Bytes 65-72  ← Needed
  - Bytes 73-84  ← Needed
  - Bytes 85-92  ← WASTED! Client already has these!

Total retransmission: 35 bytes (including duplicates)
```

#### **WITH SACK (What Actually Happened):**

```
Server receives: ACK 57 + SACK(85-92)

Server thinks:
"Client wants byte 57 AND has told me it already
has bytes 85-92. I only need to retransmit 57-84!"

Server retransmits (Frame 22):
  - Bytes 57-84 only ← Exactly what's missing!

Total retransmission: 28 bytes (no waste!)
```

**Bandwidth Saved:** 7 bytes (20% reduction in this small example, much more in real scenarios!)

---

### Frame 22: Server's Smart Retransmission

```
Frame 22: Server → Client (Retransmission)
  Seq: 57, Len: 28 bytes
  Data: Bytes 57-84  ← Only the missing data!

  TCP Analysis Flags:
    ✓ "This frame is a (suspected) retransmission"
    ✓ "RTO for this segment was: 1.536 seconds"
```

The server **selectively retransmits** only bytes 57-84 because SACK told it that bytes 85-92 were already received!

---

### Frame 23: Client Confirms Receipt

```
Frame 23: Client → Server
  ACK: 92 ← "Perfect! I now have everything up to byte 92"

  No SACK needed anymore - all data received in order!
```

---

### Visual Representation of What Happened

```
Server's Data Stream:
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
│... │ 50 │ 57 │ 64 │ 71 │ 78 │ 85 │ 92 │ 99 │...│
└────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
       ✓    ❌   ❌   ❌   ❌    ✓

Legend:
✓ = Received by client
❌ = Lost in transmission

Client's Perspective:
"I have: ...up to 56, then 85-92"
"I need: 57-84"
```

---

### TCP Header Comparison: Regular ACK vs SACK

#### **Regular ACK (Frame 19):**

```
TCP Header: 20 bytes (5 d-words)
┌──────────────┬──────────────┐
│ Source Port  │  Dest Port   │
├──────────────┴──────────────┤
│     Sequence Number          │
├──────────────────────────────┤
│  Acknowledgment Number: 57   │ ← Only this tells server what we need
├──────────────────────────────┤
│ Hdr Len │ Flags │  Window    │
├──────────────┬──────────────┤
│   Checksum   │    Urgent    │
├──────────────┴──────────────┤
│       (No Options)           │
└──────────────────────────────┘
```

#### **ACK with SACK (Frame 21):**

```
TCP Header: 32 bytes (8 d-words)
┌──────────────┬──────────────┐
│ Source Port  │  Dest Port   │
├──────────────┴──────────────┤
│     Sequence Number          │
├──────────────────────────────┤
│  Acknowledgment Number: 57   │ ← "I need byte 57"
├──────────────────────────────┤
│ Hdr Len │ Flags │  Window    │
├──────────────┬──────────────┤
│   Checksum   │    Urgent    │
├──────────────┴──────────────┤
│         Options:             │
│  NOP │ NOP │ SACK (10 bytes)│
│  Left Edge:  85              │ ← "BUT I also have 85-92!"
│  Right Edge: 92              │
└──────────────────────────────┘
```

---

### Key Observations from This Capture

1. **Cumulative ACK (57) tells what's missing**
   - "I need byte 57 next"
   - Everything before 57 was received successfully

2. **SACK (85-92) tells what was received out-of-order**
   - "I also have bytes 85-92 even though I'm missing 57-84"
   - Prevents unnecessary retransmission

3. **Header grows from 20 to 32 bytes**
   - Regular ACK: 20 bytes (minimum)
   - ACK with SACK: 32 bytes (+12 bytes for SACK option)
   - Small overhead for big efficiency gain!

4. **Multiple SACK blocks possible**
   - This example had 1 SACK block (85-92)
   - Can have up to 3-4 SACK blocks in one packet
   - Each block: 8 bytes (left edge + right edge)

---

### How to Spot SACK in Wireshark

**Filters to Use:**

```
tcp.options.sack_le          ← Shows SACK left edge
tcp.options.sack_re          ← Shows SACK right edge
tcp.analysis.retransmission  ← Shows retransmitted packets
tcp.analysis.duplicate_ack   ← Shows duplicate ACKs (often with SACK)
```

**What to Look For:**

1. **TCP Options** section in packet details
2. Header length > 20 bytes (usually 32 bytes with SACK)
3. "SACK" option with left/right edge values
4. Sequence numbers that don't match the ACK number

---

### Real-World Benefits of SACK

**Example:** Downloading a 1 MB file over a lossy network

**Scenario:** 10 packets lost out of 1,000 packets sent

**Without SACK (Go-Back-N):**

- Retransmit the 10 lost packets
- PLUS retransmit ~100 packets that came after each loss
- Total retransmissions: ~110 packets

**With SACK (Selective Repeat):**

- Retransmit ONLY the 10 lost packets
- Total retransmissions: 10 packets

**Result:** 11x more efficient! (110 vs 10 packets)

---

### Common SACK Scenarios in Real Networks

#### **Scenario 1: Single Packet Loss**

```
Sent:     1  2  X  4  5  6
Received: 1  2     4  5  6

ACK: 3, SACK(4-7)
Retransmit: packet 3 only
```

#### **Scenario 2: Multiple Non-Contiguous Losses**

```
Sent:     1  2  X  4  X  6  7  8
Received: 1  2     4     6  7  8

ACK: 3, SACK(4-5, 6-9)
         └─┬─┘  └─┬─┘
      First   Second
      block    block

Retransmit: packets 3 and 5 only
```

#### **Scenario 3: Burst Loss**

```
Sent:     1  2  X  X  X  6  7  8
Received: 1  2           6  7  8

ACK: 3, SACK(6-9)
Retransmit: packets 3, 4, 5
```

---

### Study Tips for Understanding SACK

1. **Remember the Two Parts:**
   - **ACK number** = "I need this sequence number next" (cumulative)
   - **SACK blocks** = "But I also already have these ranges" (selective)

2. **SACK is Always Optional:**
   - Must be negotiated during handshake (SYN/SYN-ACK)
   - Both sides must support it
   - Not all TCP implementations use it

3. **SACK Doesn't Replace ACK:**
   - SACK **supplements** the regular ACK
   - ACK number still indicates the "edge" of received data
   - SACK fills in the "holes" beyond that edge

4. **Look for the Pattern:**
   - Duplicate ACK with same ACK number
   - But packet has SACK option
   - Followed by selective retransmission

---

### Practice Questions

1. **If ACK=100 and SACK(150-200, 250-300), what bytes are missing?**
   - Answer: Bytes 100-149 and 200-249

2. **Why does the TCP header grow when SACK is used?**
   - Answer: SACK is an optional field added to the options section

3. **Can you have SACK without packet loss?**
   - Answer: No, SACK only appears when there's out-of-order delivery

4. **What's the maximum number of SACK blocks in one packet?**
   - Answer: Typically 3-4 blocks (limited by TCP options space of 40 bytes)

---

## Understanding SACK: Left Edge and Right Edge Explained

### What are Left Edge and Right Edge?

When TCP uses SACK (Selective Acknowledgment), it tells the sender about **ranges of data** that have been successfully received out-of-order. Each range is defined by two boundaries:

**Left Edge** = The starting sequence number of received data  
**Right Edge** = The ending sequence number of received data (first byte NOT received after this block)

Think of it like highlighting text in a document:

- **Left Edge**: Where you START highlighting
- **Right Edge**: Where you STOP highlighting

### Example from Real Capture (SACK*example*.pcapng):

```
SACK Option: Left Edge = 85, Right Edge = 92

What this means:
├─────────────────────────────────────────────┤
│   Missing    │    Received    │   Unknown  │
├─────────────────────────────────────────────┤
   (before 85)      85-91         (after 92)
                     ↑             ↑
                  Left Edge    Right Edge
```

**Translation:** "I have successfully received bytes 85, 86, 87, 88, 89, 90, and 91"

**Important:** The right edge (92) is **NOT included** - it's the first byte AFTER the block.

**Formula:**

```
Bytes in SACK block = Right Edge - Left Edge
Example: 92 - 85 = 7 bytes received in this block
```

### Why Two Values (Left & Right)?

Because we need to specify a **range**, not just a single byte:

```
Single byte received (byte 85):
  Left Edge = 85
  Right Edge = 86  (one byte range: just byte 85)

Multiple bytes received (bytes 85-91):
  Left Edge = 85
  Right Edge = 92  (seven byte range: 85,86,87,88,89,90,91)
```

### Multiple SACK Blocks Example:

```
ACK: 100
SACK Block 1: Left Edge = 150, Right Edge = 200
SACK Block 2: Left Edge = 250, Right Edge = 300

Visual representation:
0────100───────150──200───────250──300─────→
     ↑          ↑────┤          ↑────┤
   Need this   Have this      Have this
   (and 101+)  (150-199)      (250-299)

Missing bytes:
- 100-149 (50 bytes)
- 200-249 (50 bytes)

Total missing: 100 bytes
```

---

## 🔬 CRITICAL COMPARISON: SACK Enabled vs SACK Disabled

Let's compare **two real captures** showing the SAME type of packet loss scenario:

1. **SACK*example*.pcapng** - SACK enabled and working
2. **SACK_disabled.pcapng** - SACK disabled/refused

### SACK Negotiation During Handshake

SACK must be **negotiated** during the TCP handshake. BOTH sides must agree!

#### **SACK*example*.pcapng (SACK Works):**

```
Frame 1: Client → Server [SYN]
  TCP Options: MSS=1460, SACK permitted ✓
  Client: "I support SACK, do you?"

Frame 2: Server → Client [SYN-ACK]
  TCP Options: MSS=1460, SACK permitted ✓
  Server: "Yes! I support SACK too!"

Frame 3: Client → Server [ACK]
  Connection established with SACK enabled

✅ BOTH sides agreed to use SACK!
```

#### **SACK_disabled.pcapng (SACK Refused):**

```
Frame 1: Client → Server [SYN]
  TCP Options: MSS=1460, SACK permitted ✓
  Client: "I support SACK, do you?"

Frame 2: Client → Server [SYN retransmit]
  TCP Options: MSS=1460, SACK permitted ✓
  Client: "Hey, I support SACK..."

Frame 3: Server → Client [SYN-ACK]
  TCP Options: MSS=1460, NO SACK ❌
  Server: "Sorry, I don't support SACK"
  ⚠️ Wireshark: "The SYN packet does not contain a SACK PERM option"

Frame 4: Client → Server [ACK]
  Connection established WITHOUT SACK

❌ Server REFUSED SACK - falling back to regular ACK only!
```

**Key Point:** Even if the client wants SACK, if the server doesn't include "SACK permitted" in its SYN-ACK, SACK cannot be used for the entire connection!

---

### The Results: Dramatic Difference!

| Metric                      | WITH SACK                       | WITHOUT SACK             |
| --------------------------- | ------------------------------- | ------------------------ |
| **Total Packets**           | 39                              | 26                       |
| **Total Retransmissions**   | **1** ✓                         | **5** ❌                 |
| **Retransmission Strategy** | Selective (smart)               | Timeout-based (blind)    |
| **Recovery Time**           | Fast (~2 seconds)               | Slow (multiple timeouts) |
| **Bandwidth Waste**         | Minimal                         | Significant              |
| **Server Knowledge**        | ✅ Knows exactly what's missing | ❌ No idea what arrived  |

### Visual Timeline Comparison

#### WITH SACK (Efficient):

```
SACK_example_.pcapng

Retransmissions: 1
Frame 22: Selective retransmission of missing data only

Time →
0────────20────────40────────60────────70
│    Data Flow     │ Loss │SACK│Fix│Done│
│   (normal)       │      │Tell│ 1 │    │
└──────────────────┴──────┴────┴───┴────┘
                   ↑          ↑
                Problem   Quick Fix
```

#### WITHOUT SACK (Inefficient):

```
SACK_disabled.pcapng

Retransmissions: 5
Frames 2, 14, 17, 18, 20: Multiple retransmission attempts

Time →
0───10───20───30───40───50───60───70
│Data│TO│Retry│TO│Retry│TO│Retry│Done│
│    │  │  1  │  │  2  │  │  3  │    │
└────┴──┴─────┴──┴─────┴──┴─────┴────┘
     ↑        ↑        ↑
  Problem  Retry 1  Retry 2  Retry 3...

TO = Timeout (1-3 seconds each)
```

**Result:** SACK version completes faster with fewer retransmissions!

---

### Why Such a Difference?

#### **WITH SACK (Frame 21 in SACK*example*.pcapng):**

```
Client → Server:
  ACK: 57  ← "I need byte 57"
  SACK: Left Edge = 85, Right Edge = 92  ← "BUT I have 85-92!"

Server thinks:
  "Ah! They need 57-84, but they already have 85-92.
   I'll ONLY retransmit 57-84. No waste!"

Result: 1 smart retransmission
```

#### **WITHOUT SACK (Frames 13-20 in SACK_disabled.pcapng):**

```
Frame 13: Client sends seq 7
Frame 14: Retransmit seq 7 (no response, timeout)
Frame 15: Server finally ACKs 9

Frame 16: Client sends seq 9
Frame 17: Retransmit seq 9 (timeout)
Frame 18: Retransmit seq 9 AGAIN (timeout again!)
Frame 19: Server ACKs 13
Frame 20: Server retransmits seq 9 (just in case)

Server thinks:
  "I have no idea what they received. Better keep trying
   everything until I get an ACK..."

Result: 5 blind retransmissions + wasted time
```

---

### SACK Option Structure in Detail

When you see SACK in a packet, here's the actual TCP option structure:

```
TCP Options Field (in Frame 21):
┌────────────────────────────────────────────────┐
│ NOP (1 byte) - padding for alignment          │
├────────────────────────────────────────────────┤
│ NOP (1 byte) - padding for alignment          │
├────────────────────────────────────────────────┤
│ Kind: 5 (1 byte) ← This identifies SACK       │
├────────────────────────────────────────────────┤
│ Length: 10 (1 byte) ← 2 + 4 + 4 = 10 bytes    │
├────────────────────────────────────────────────┤
│ Left Edge: 85 (4 bytes) ← Start sequence #    │
├────────────────────────────────────────────────┤
│ Right Edge: 92 (4 bytes) ← End sequence #     │
└────────────────────────────────────────────────┘

Total: 12 bytes (2 NOP + 10 SACK)
Header grows from 20 bytes to 32 bytes
```

**Multiple Blocks Example:**

```
Kind: 5
Length: 26  ← (2 header + 8×3 blocks = 26 bytes for 3 blocks)

Block 1: Left=100, Right=150  (8 bytes)
Block 2: Left=200, Right=250  (8 bytes)
Block 3: Left=300, Right=350  (8 bytes)

Each block = 4 bytes (left) + 4 bytes (right) = 8 bytes
Maximum ~3-4 blocks per packet (TCP options limited to 40 bytes)
```

---

### How to Verify SACK in Wireshark

#### **Check During Handshake:**

```
Filter: tcp.flags.syn == 1

Look at SYN and SYN-ACK packets:
1. Expand: Transmission Control Protocol → Options
2. Look for: "TCP Option - SACK permitted"

   ✅ Present in BOTH SYN and SYN-ACK = SACK enabled
   ❌ Missing in SYN-ACK = SACK disabled for connection
```

#### **Check During Data Transfer:**

```
Filter: tcp.options.sack_le

If packets appear → SACK is being used actively
If empty → SACK not negotiated or no packet loss yet

Look for:
- "TCP Option - SACK"
- "left edge = X"
- "right edge = Y"
```

#### **Compare Retransmission Patterns:**

```
Filter: tcp.analysis.retransmission

Count retransmissions:
- WITH SACK: Few, targeted (usually 1-2 per lost packet)
- WITHOUT SACK: Many, repeated (3-5+ per lost packet)
```

---

### Real-World Impact

**Scenario:** 10 MB file transfer over WiFi with 2% packet loss

**With SACK:**

```
Packets lost: ~200
Retransmissions: ~200 (one per loss)
Extra time: ~2 seconds
Total time: ~10 seconds
Efficiency: 95%
```

**Without SACK:**

```
Packets lost: ~200
Retransmissions: ~600-800 (multiple attempts)
Extra time: ~15-20 seconds (timeouts)
Total time: ~25-30 seconds
Efficiency: 40%
```

**Result:** SACK is **2.5-3x faster** on lossy networks!

---

### Practice Exercise: Decode This SACK

```
You see in Wireshark:
ACK Number: 5000
SACK Block 1: Left Edge = 6000, Right Edge = 6500
SACK Block 2: Left Edge = 7000, Right Edge = 7200

Questions:
1. What bytes does the receiver need?
2. What bytes does the receiver already have?
3. How many bytes are missing total?
4. How many SACK blocks are present?
5. What should the sender retransmit?

Answers:
1. Receiver needs: 5000-5999 and 6500-6999
2. Receiver already has: 6000-6499 (500 bytes) and 7000-7199 (200 bytes)
3. Missing: 1500 bytes total (1000 + 500)
4. SACK blocks: 2
5. Sender should retransmit: bytes 5000-5999 and 6500-6999 only
```

---

### Data Size Units (for reference)

- **1 bit** → can store a binary value (0 or 1)
  - 1 byte = 8 bits
  - 4 bits = 1 nibble/nybble
- **8 bits (1 byte)** → a char
- **16 bits** → a short or word
- **32 bits** → d-word (double word) or long
- **64 bits** → q-word (quad word)

**ASCII**: up to 255 values (8 bits)

**We usually count things in d-words (32-bit units)**

---

## UDP (User Datagram Protocol)

### UDP Characteristics

UDP provides **unreliable transfer of groups of bytes ("datagrams")** between client and server.

**Connectionless**:

- **No "connection"** between client & server
- **No handshaking** before sending data
- Sender explicitly attaches IP destination address and port number to each packet
- Receiver extracts sender IP address and port number from received packet

**Unreliable**:

- Transmitted data may be **lost** or received **out-of-order**
- No guarantee of delivery
- Data may be lost; is okay if you lose some data

**Lightweight**:

- Faster than TCP
- Minimal protocol overhead
- **Faster, lightweight** transport protocol

**Use cases**:

- **DNS** uses UDP
- **Live streaming** (live broadcasts)
  - Needs to be fast
  - Okay if you lose some data
  - More interested in getting updates than recovering all lost data
- Applications that need speed over reliability

---

### UDP Segment Header

**Simple structure** (only 8 bytes total):

1. **Source port #** (16 bits)
2. **Destination port #** (16 bits)
3. **Length** (16 bits)
   - Length in bytes of UDP segment, including header
4. **Checksum** (16 bits)
5. **Application data (payload)** (variable length)

**Much simpler than TCP** - just 4 header fields vs TCP's many fields

---

### UDP Checksum

**Goal**: Detect "errors" (flipped bits) in transmitted segment

**Sender**:

1. Treat segment contents (including header fields) as sequence of 16-bit integers
2. **Checksum**: addition (one's complement sum) of segment contents
3. Sender puts checksum value into UDP checksum field

**Receiver**:

1. Compute checksum of received segment
2. Check if computed checksum equals checksum field value:
   - **NO** = error detected
   - **YES** = no error detected (but maybe errors nonetheless - not foolproof!)

**Example**: Add two 16-bit integers

```
  1 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0
  1 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
 ___________________________________
wraparound → 1 1 0 1 1 1 0 1 1 1 0 1 1 1 0 1 1
                ↓
sum:     1 0 1 1 1 0 1 1 1 0 1 1 1 1 0 0
checksum: 0 1 0 0 0 1 0 0 0 1 0 0 0 0 1 1
```

**Note**: When adding numbers, a carryout from the most significant bit needs to be added to the result (wraparound)

**At receiver**: All three 16-bit values (including checksum) are added

- If result is **1111111111111111** → no errors
- If any bit is **0** → errors in packet

**Important**:

- UDP provides error **checking**
- But doesn't do anything to **recover** from error!
- UDP can either:
  a. Discard the damaged segment
  b. Pass damaged segment to application with a warning

---

## Why Choose UDP Instead of TCP?

### Advantages of UDP:

1. **Best control over when data is sent**
   - No congestion control = no delays
   - Application has direct control

2. **No connection establishment**
   - Quick! Imagine DNS with three-way handshaking like TCP?
   - No handshaking delay

3. **Small header size**
   - **TCP**: 20 bytes minimum
   - **UDP**: 8 bytes
   - Less overhead

4. **No connection state**
   - Server doesn't maintain connection information
   - Can support more clients

---

## Popular Applications and Underlying Transport Protocol

| Application            | Application-Layer Protocol | Underlying Transport Protocol |
| ---------------------- | -------------------------- | ----------------------------- |
| Electronic mail        | SMTP                       | **TCP**                       |
| Remote terminal access | Telnet                     | **TCP**                       |
| Web                    | HTTP                       | **TCP**                       |
| File transfer          | FTP                        | **TCP**                       |
| Remote file server     | NFS                        | Typically **UDP**             |
| Streaming multimedia   | Typically proprietary      | **UDP or TCP**                |
| Internet telephony     | Typically proprietary      | **UDP or TCP**                |
| Network management     | SNMP                       | Typically **UDP**             |
| Routing protocol       | RIP                        | Typically **UDP**             |
| Name translation       | DNS                        | Typically **UDP**             |

---

## TCP Scenarios - What Happens?

### Scenario Analysis (from slide 20):

1. **Lost ACK during handshake**: Client resends SYN after timeout
2. **Lost SYN-ACK**: Client resends SYN after timeout
3. **Lost payload**: Sender resends after timeout
4. **Lost ACK for payload**: Sender resends payload after timeout
5. **Out-of-order segments**: TCP handles using sequence numbers, buffers and reorders
6. **Checksum error**: Segment discarded, sender will timeout and retransmit

**Note**: Check the SACK (Selective Acknowledgment) pcap files mentioned to see how TCP handles out-of-order segments in practice

---

## Key Takeaways

### TCP vs UDP Quick Comparison:

| Feature        | TCP                        | UDP                       |
| -------------- | -------------------------- | ------------------------- |
| Connection     | Connection-oriented        | Connectionless            |
| Reliability    | Reliable                   | Unreliable                |
| Ordering       | In-order delivery          | No ordering guarantee     |
| Speed          | Slower (overhead)          | Faster (minimal overhead) |
| Header size    | 20+ bytes                  | 8 bytes                   |
| Error recovery | Yes (retransmission, SACK) | No recovery               |
| Use case       | When reliability needed    | When speed needed         |
| Examples       | HTTP, FTP, Email           | DNS, Streaming, VoIP      |

---

## Additional Notes to Review

- Practice drawing the TCP three-way handshake
- Understand the 4-tuple that identifies a TCP connection
- **Review the SACK pcap files** mentioned to see real examples of selective acknowledgment in action
- Know when to use TCP vs UDP for different applications
- Understand how sequence numbers and ACKs work together
- **Understand the difference between cumulative ACK and SACK** - this is important!

---

## Study Tips

1. **Draw diagrams**: Especially for the three-way handshake and segment structures
2. **Compare and contrast**: Make sure you understand TCP vs UDP differences
3. **Practice scenarios**: Work through what happens when packets are lost
4. **Understand the "why"**: Know why certain design choices were made (e.g., why UDP for DNS)
5. **Real-world examples**: Think about which protocol different apps use and why
6. **Analyze the SACK pcap file**: Open `SACK_example_.pcapng` in Wireshark and follow along with the notes
   - Look at Frame 21 to see SACK in action
   - Compare Frame 19 (regular ACK) with Frame 21 (ACK + SACK)
   - Notice how Frame 22 only retransmits the missing data
   - Use filter: `tcp.options.sack_le` to highlight SACK packets
7. **Understand sequence numbers**: Practice calculating what ACK number should be based on sequence numbers and data length

---

## Quick Reference: ACK vs SACK

| Feature                     | Regular ACK                          | SACK (Selective ACK)                     |
| --------------------------- | ------------------------------------ | ---------------------------------------- |
| **What it indicates**       | Next byte expected (cumulative)      | Specific ranges already received         |
| **Header size**             | 20 bytes (minimum)                   | 32+ bytes (includes options)             |
| **When used**               | Every TCP packet                     | Only when out-of-order packets received  |
| **Information provided**    | "I need byte X next"                 | "I need byte X, BUT I have bytes Y-Z"    |
| **Retransmission behavior** | May retransmit already-received data | Only retransmits what's actually missing |
| **Efficiency**              | Lower (Go-Back-N style)              | Higher (Selective Repeat style)          |
| **Negotiated**              | No (always present)                  | Yes (during handshake)                   |
| **TCP Option Kind**         | N/A                                  | Kind = 5                                 |
| **Example**                 | ACK=100                              | ACK=100, SACK(150-200)                   |
| **Wireshark filter**        | `tcp.ack`                            | `tcp.options.sack_le`                    |

### Quick Formulas:

```
ACK Number = Last Received Seq + Data Length
Next Expected Byte = ACK Number
Bytes Missing = (SACK Left Edge) - (ACK Number)

Example:
Received: Seq=50, Len=7
ACK = 50 + 7 = 57 (expecting byte 57 next)

If next packet is Seq=85:
Missing bytes = 85 - 57 = 28 bytes (seq 57-84)
SACK would indicate: SACK(85-92)
```

---

_End of Transport Layer Notes_
