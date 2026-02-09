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
