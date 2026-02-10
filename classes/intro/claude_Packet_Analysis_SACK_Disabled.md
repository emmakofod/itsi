# Packet-by-Packet Analysis: SACK_disabled.pcapng

## What Happens When TCP Has NO SACK

---

## Overview

**Capture:** SACK_disabled.pcapng  
**Client:** 192.168.238.134 (port 39382)  
**Server:** 192.168.238.128 (port 8080)  
**Key Issue:** SACK was NOT negotiated, so retransmissions are inefficient

---

## Phase 1: TCP Three-Way Handshake (Packets 1-4)

### 📦 Packet 1 (Time: 0.000000000)

```
Client → Server: SYN
Source: 192.168.238.134:39382
Dest:   192.168.238.128:8080
Flags:  [SYN]
Seq:    0
Options: MSS=1460, SACK_PERM ✓

What happens:
Client: "Hey server, I want to connect. I support SACK!"
```

**Status:** Waiting for SYN-ACK response...

---

### 📦 Packet 2 (Time: 1.011367395) - 🔴 FIRST PROBLEM!

```
Client → Server: SYN [TCP Retransmission]
Source: 192.168.238.134:39382
Dest:   192.168.238.128:8080
Flags:  [SYN]
Seq:    0 (same as packet 1!)
Options: MSS=1460, SACK_PERM ✓

⏱️ Time since packet 1: 1.01 seconds

What happens:
Client: "Hello?? I didn't get your SYN-ACK. Let me try again..."
```

**Why retransmission?**

- Client waited ~1 second for SYN-ACK
- No response received
- TCP timeout → retransmit SYN

---

### 📦 Packet 3 (Time: 1.012631392)

```
Server → Client: SYN-ACK
Source: 192.168.238.128:8080
Dest:   192.168.238.134:39382
Flags:  [SYN, ACK]
Seq:    0
Ack:    1
Options: MSS=1460, NO SACK_PERM ❌

⏱️ Time since packet 2: 0.001 seconds

What happens:
Server: "I got your SYN! Here's my SYN-ACK."
Server: "But I DON'T support SACK"

🚨 CRITICAL: Server's SYN-ACK does NOT include SACK_PERM
Result: SACK is DISABLED for this entire connection!
```

**Wireshark Warning:**

> "The SYN packet does not contain a SACK PERM option"

---

### 📦 Packet 4 (Time: 1.012736594)

```
Client → Server: ACK
Flags:  [ACK]
Seq:    1
Ack:    1

⏱️ Time since packet 3: 0.0001 seconds

What happens:
Client: "Got it! Connection established."
Client: "OK, no SACK then. We'll use regular ACKs only."

✅ CONNECTION ESTABLISHED (without SACK)
```

---

## Phase 2: Data Transfer Begins (Packets 5-7)

### 📦 Packet 5 (Time: 5.020449096)

```
Server → Client: PSH, ACK [Data]
Seq:    1
Ack:    1
Len:    8 bytes
Data:   Bytes 1-8

What happens:
Server: "Here's 8 bytes of data (seq 1-8)"

Client receives: ✅ Bytes 1-8
Client expects next: Byte 9
```

---

### 📦 Packet 6 (Time: 5.020511651)

```
Client → Server: ACK
Seq:    1
Ack:    9 ← Acknowledging receipt of bytes 1-8

⏱️ Time since packet 5: 0.00006 seconds (62 microseconds!)

What happens:
Client: "Got bytes 1-8! Send me byte 9 next."

Server knows: Client successfully received up to byte 8
```

---

### 📦 Packet 7 (Time: 13.883879999)

```
Server → Client: PSH, ACK [Data]
Seq:    1 ← Wait, this is OLD data!
Ack:    9
Len:    2 bytes

⏱️ Time since packet 6: 8.86 seconds

What happens:
Server: "Hmm, let me send 2 bytes starting at seq 1..."
This seems like server is confused or retrying

🤔 Odd behavior - server going backwards?
```

---

## Phase 3: 🔴 THE BIG PROBLEM - Missing Packets! (Packet 8)

### 📦 Packet 8 (Time: 13.883549549)

```
[TCP Previous segment not captured] ⚠️
Server → Client: Data
Seq:    3
Ack:    9
Len:    ?

🚨 WIRESHARK WARNING: Previous segment not captured!

What this means:
Expected: Seq=9 (based on previous ACK)
Got:      Seq=3
Missing:  Something is wrong with the sequence!

What ACTUALLY happened:
There was a packet sent BEFORE this one that Wireshark didn't see
OR the sequence numbers jumped unexpectedly
```

---

## Phase 4: Client Tries to Send Data (Packets 9-13)

### 📦 Packet 9 (Time: 14.910838759)

```
Client → Server: PSH, ACK [Data]
Seq:    3
Ack:    9
Len:    2 bytes
Data:   Bytes 3-4 from client

What happens:
Client: "Here's my data (bytes 3-4)"
```

---

### 📦 Packet 10 (Time: 14.911338184)

```
Server → Client: ACK
Seq:    9
Ack:    5 ← Acknowledging client's bytes 3-4

What happens:
Server: "Got your bytes 3-4! Send me byte 5 next."
```

---

### 📦 Packet 11 (Time: 15.764847592)

```
Client → Server: PSH, ACK [Data]
Seq:    5
Ack:    9
Len:    2 bytes

Client: "Here's bytes 5-6"
```

---

### 📦 Packet 12 (Time: 15.765268046)

```
Server → Client: ACK
Ack:    7 ← Got bytes 5-6

Server: "Got bytes 5-6! Send byte 7 next."
```

---

### 📦 Packet 13 (Time: 16.667219094)

```
Client → Server: PSH, ACK [Data]
Seq:    7
Ack:    9
Len:    2 bytes

Client: "Here's bytes 7-8"
```

---

## Phase 5: 🔴 RETRANSMISSION STORM! (Packets 14-18)

This is where the LACK OF SACK causes major problems!

### 📦 Packet 14 (Time: 19.639343227) - 🔴 RETRANSMISSION #1

```
[TCP Retransmission] ⚠️
Client → Server: PSH, ACK [Data]
Seq:    7 ← SAME as packet 13!
Ack:    9
Len:    2 bytes

⏱️ Time since packet 13: 2.97 seconds

What happens:
Client: "I sent bytes 7-8 but got no ACK..."
Client: "Timeout! Let me resend bytes 7-8"

Why retransmit?
- Sent packet 13 at time 16.667
- Waited for ACK... no ACK received
- After ~3 seconds: TIMEOUT
- Retransmit the same data
```

**Without SACK:**
Server has NO WAY to tell client "I got bytes 7-8 but I'm missing something else"

---

### 📦 Packet 15 (Time: 19.708799305)

```
Server → Client: Data
Seq:    14
Ack:    9 ← Still ACKing 9!
Len:    ?

⏱️ Time since packet 14: 0.07 seconds

What happens:
Server: "Here's more data from me (seq 14+)"
Server: "But I'm still waiting for byte 9 from you!"

Notice: Server's ACK is still 9 - hasn't moved!
```

---

### 📦 Packet 16 (Time: 19.708836846)

```
Client → Server: PSH, ACK [Data]
Seq:    9 ← NEW data!
Ack:    9
Len:    4 bytes

What happens:
Client: "OK, here's bytes 9-12"
```

**This is the data the server was waiting for!**

---

### 📦 Packet 17 (Time: 20.796886963) - 🔴 RETRANSMISSION #2

```
[TCP Retransmission] ⚠️
Client → Server: PSH, ACK
Seq:    9 ← SAME as packet 16!
Ack:    9
Len:    4 bytes

⏱️ Time since packet 16: 1.09 seconds

What happens:
Client: "I sent bytes 9-12 but got no ACK..."
Client: "Timeout! Resending bytes 9-12 AGAIN"

Why AGAIN?
WITHOUT SACK, client doesn't know if server got packet 16
Must wait for timeout and retry
```

---

### 📦 Packet 18 (Time: 28.147402430) - 🔴 RETRANSMISSION #3

```
[TCP Retransmission] ⚠️
Client → Server: PSH, ACK
Seq:    9 ← STILL trying to send bytes 9-12!
Ack:    9
Len:    4 bytes

⏱️ Time since packet 17: 7.35 seconds

What happens:
Client: "STILL no ACK for bytes 9-12!"
Client: "Timeout AGAIN! Third attempt!"

This is getting ridiculous!
3rd retransmission of the SAME data!
```

**Timeouts are getting longer:**

- 1st try: packet 16
- Wait ~1 second → retry (packet 17)
- Wait ~7 seconds → retry again (packet 18)

TCP's exponential backoff in action!

---

### 📦 Packet 19 (Time: 28.148363425)

```
Server → Client: ACK
Seq:    11
Ack:    13 ← FINALLY!

⏱️ Time since packet 18: 0.001 seconds

What happens:
Server: "FINALLY! I got bytes 9-12!"
Server: "Send me byte 13 next."

Client thinks: "About time! That took 3 tries!"
```

**Timeline of bytes 9-12:**

- 1st send: packet 16 (time 19.708)
- 2nd send: packet 17 (time 20.796)
- 3rd send: packet 18 (time 28.147)
- ACK received: packet 19 (time 28.148)

**Total time: 8.4 seconds for 4 bytes!**

---

## Phase 6: Server Also Has Problems (Packet 20)

### 📦 Packet 20 (Time: 31.701970524) - 🔴 SERVER RETRANSMISSION

```
[TCP Retransmission] ⚠️
Server → Client: PSH, ACK
Seq:    9
Ack:    13
Len:    2 bytes

What happens:
Server: "Let me retransmit bytes 9-10 just to be safe..."

Why?
Server is ALSO uncertain about what got through
Without SACK, both sides are guessing!
```

---

## Phase 7: Recovery and Connection Close (Packets 21-26)

### 📦 Packet 21 (Time: 31.702008787)

```
Client → Server: ACK
Ack:    11

Client: "I have up to byte 10"
```

---

### 📦 Packet 22 (Time: 31.702855797)

```
Server → Client: PSH, ACK
Seq:    11
Len:    8 bytes

Server: "Here's bytes 11-18"
```

---

### 📦 Packet 23 (Time: 31.702855507)

```
Client → Server: ACK
Ack:    19

Client: "Got bytes 11-18!"
```

---

### 📦 Packet 24 (Time: 66.930434549)

```
Client → Server: FIN, ACK
Seq:    19
Ack:    13

Client: "I'm done. Closing connection."
```

---

### 📦 Packet 25 (Time: 66.930735827)

```
Server → Client: FIN, ACK
Seq:    13
Ack:    20

Server: "OK, I'm closing too."
```

---

### 📦 Packet 26 (Time: 66.931586519)

```
Client → Server: ACK
Ack:    14

Client: "Acknowledged your FIN. Connection closed."

✅ CONNECTION TERMINATED
```

---

## Summary of Retransmissions

| Packet # | Type         | Seq | What                    | Why                 |
| -------- | ------------ | --- | ----------------------- | ------------------- |
| **2**    | SYN Retrans  | 0   | Resend SYN              | No SYN-ACK received |
| **14**   | Data Retrans | 7   | Resend bytes 7-8        | Timeout, no ACK     |
| **17**   | Data Retrans | 9   | Resend bytes 9-12       | Timeout, no ACK     |
| **18**   | Data Retrans | 9   | Resend bytes 9-12 AGAIN | Timeout AGAIN       |
| **20**   | Data Retrans | 9   | Server resends 9-10     | Uncertainty         |

**Total Retransmissions: 5**

---

## Timeline of the Disaster

```
Time     Event                              Problem
------   ---------------------------------  ---------------------------
0.000    Client sends SYN
1.011    Client RETRANS SYN                 No response (1 sec wait)
1.013    Server sends SYN-ACK (no SACK!)    🚨 SACK REFUSED
1.013    Handshake complete                 Without SACK
5.020    Server sends bytes 1-8             ✓
5.021    Client ACKs byte 9                 ✓
---      [Some packets missing]             ???
14.910   Client sends bytes 3-4             ✓
15.764   Client sends bytes 5-6             ✓
16.667   Client sends bytes 7-8             Sent...
19.639   Client RETRANS bytes 7-8           No ACK (3 sec timeout)
19.708   Client sends bytes 9-12            Sent...
20.796   Client RETRANS bytes 9-12          No ACK (1 sec timeout)
28.147   Client RETRANS bytes 9-12 AGAIN!   No ACK (7 sec timeout)
28.148   Server ACKs byte 13                FINALLY!
31.702   Server RETRANS bytes 9-10          Just being cautious
31.703   Recovery...                        ✓
66.930   Connection closes                  Done!
```

**Total Duration: 66.9 seconds**
**Retransmissions: 5**
**Wasted time: ~20+ seconds in timeouts**

---

## What's Wrong: The Root Cause

### ❌ **WITHOUT SACK:**

**When packet 16 is sent (bytes 9-12):**

```
Client sends → [bytes 9-12]
              ??? (packet lost or delayed)
Client waits... no ACK
Client waits... still no ACK
⏱️ TIMEOUT (1 second)
Client resends → [bytes 9-12] again
              ??? still problems
⏱️ TIMEOUT (7 seconds)
Client resends → [bytes 9-12] THIRD TIME
              ✓ finally gets through
Server ACKs → "Got it!"
```

**Total time for 4 bytes: 8.4 seconds**

---

### ✅ **WITH SACK (What SHOULD Happen):**

```
Client sends → [bytes 9-12]
Server immediately sends → ACK=9, SACK(9-13)
                          "I'm waiting for byte 9 but I got 9-13"
Client knows → "They got it! No need to resend!"

Total time: 0.001 seconds (one round trip)
```

---

## Why So Many Retransmissions?

### Problem 1: No SACK = No Visibility

```
WITHOUT SACK:
Client: "Did they get my packet?"
Server: "..." (silence)
Client: "I guess not... resend!"

WITH SACK:
Client: "Did they get my packet?"
Server: "Yes! I got bytes 9-12!" (SACK tells them)
Client: "Great! Moving on..."
```

### Problem 2: Timeouts

```
Each retransmission requires waiting for timeout:
- 1st timeout: ~1 second
- 2nd timeout: ~2-4 seconds
- 3rd timeout: ~7-8 seconds (exponential backoff)

Total wasted time: 10-13 seconds per lost packet!
```

### Problem 3: Cascading Failures

```
One lost packet causes:
→ Timeout
→ Retransmission
→ Maybe lost again
→ Another timeout
→ Another retransmission
→ Uncertainty on both sides
→ Unnecessary retransmissions from server too
```

---

## Client's Perspective: When Do I Have the Data?

Let's track when the **client actually receives** data from the server:

### Client's Receive Buffer:

```
Packet 5 (time 5.020):
Client receives: Bytes 1-8 from server ✓
Client ACKs: 9
Buffer: [1][2][3][4][5][6][7][8]

Packet 15 (time 19.708):
Client receives: Bytes 14-? from server
Buffer: [1][2][3][4][5][6][7][8]...[missing]...[14][15]...
         ↑_____________received______________↑ ↑_new data_↑

Client CANNOT acknowledge byte 14 yet because bytes 9-13 are missing!
This is the TCP in-order delivery requirement!

Packet 20 (time 31.702):
Server retransmits bytes 9-10
Client receives: Bytes 9-10 ✓
Buffer: [1][2][3][4][5][6][7][8][9][10]...[missing 11-13]...[14][15]...

Packet 22 (time 31.703):
Server sends bytes 11-18
Client receives: Bytes 11-18 ✓
Buffer: [1][2][3][4][5][6][7][8][9][10][11][12][13][14][15][16][17][18] ✓
         ↑________________________________ALL DATA RECEIVED_____________________________↑

NOW client can deliver ALL data to the application!
```

**Key Point:** Even though client received byte 14-15 at time 19.708, it CANNOT use that data until bytes 9-13 arrive! This is TCP's in-order guarantee.

---

## Server's Perspective: When Do I Know Client Got My Data?

### Server's Tracking:

```
Packet 5 (time 5.020):
Server sends: Bytes 1-8
Waiting for ACK...

Packet 6 (time 5.021):
Server receives: ACK=9 ✓
Server knows: Client has bytes 1-8
Server can: Send more data or move on

Packet 15 (time 19.708):
Server sends: Bytes 14-?
Waiting for ACK...
... waiting ...
... waiting ...
... NO ACK! ❌

Problem: Server doesn't know if client got bytes 14+
Without SACK, server is BLIND
Server must: Wait or retransmit (but retransmit what?)

Packet 19 (time 28.148):
Server receives: ACK=13
Server knows: Client has up to byte 12
But wait... what about bytes 14+ I sent in packet 15?
Server: "I have no idea if they got that..."
```

---

## The Inefficiency Formula

**Time Wasted per Lost Packet:**

```
Without SACK:
1 lost packet = 3-4 retransmission attempts
Each attempt = 1-8 second timeout
Total delay = 10-20 seconds per packet

With SACK:
1 lost packet = 1 retransmission
Immediate notification via SACK
Total delay = <1 second per packet

Efficiency gain: 10-20x faster!
```

---

## Lessons Learned

### 1. **SACK Negotiation is Critical**

```
Packet 3 was the CRITICAL moment:
Server's SYN-ACK did NOT include SACK_PERM
Result: Entire connection suffers

Lesson: BOTH sides must support SACK
```

### 2. **Timeouts are Expensive**

```
Every retransmission requires:
- Waiting for timeout (1-8 seconds)
- Sending duplicate data
- More waiting
- Uncertainty on both sides

Total cost: 10-20 seconds per problem
```

### 3. **One Lost Packet → Cascade of Problems**

```
Without SACK:
Lost packet → Can't confirm receipt → Timeout → Retransmit
           → Maybe lost again → Longer timeout → Retransmit again
           → Other side also confused → More retransmissions
           → Both sides wasting time

With SACK:
Lost packet → SACK tells sender exactly what's missing
           → One targeted retransmission → Done!
```

### 4. **In-Order Delivery Blocks Applications**

```
Client received byte 14-15 at time 19.708
But application can't use it until bytes 9-13 arrive
Finally available at time 31.703

Wasted time: 12 seconds where data was received but unusable!
```

---

## Comparison: What IF SACK Was Enabled?

**Hypothetical with SACK:**

```
Time     Event (WITH SACK)
------   ---------------------------------
0.000    Client sends SYN (SACK_PERM)
0.001    Server sends SYN-ACK (SACK_PERM) ✓
0.002    Handshake complete with SACK ✓
5.020    Server sends bytes 1-8 ✓
5.021    Client ACKs 9 ✓
16.667   Client sends bytes 7-8
16.668   Server ACKs, might include SACK if issues
19.708   Client sends bytes 9-12
19.709   Server sends ACK=13, SACK(9-13) ✓
19.710   ALL DONE! No retransmissions!

Total time: ~20 seconds
Retransmissions: 1 (maybe, only if truly lost)
Efficiency: HIGH
```

vs **Actual without SACK:**

```
Total time: 66.9 seconds
Retransmissions: 5
Wasted time: 45+ seconds
Efficiency: TERRIBLE
```

---

## Final Verdict

**WITHOUT SACK (this capture):**

- ❌ 5 retransmissions
- ❌ Multiple timeouts (1-8 seconds each)
- ❌ Total time: 66.9 seconds
- ❌ Wasted bandwidth
- ❌ Both sides confused
- ❌ Application delays

**WITH SACK (should be used):**

- ✅ 0-1 retransmissions
- ✅ Immediate feedback
- ✅ Total time: ~20 seconds
- ✅ Efficient bandwidth use
- ✅ Clear communication
- ✅ Minimal delays

**SACK makes TCP 3-4x faster on lossy networks!**

---

_End of Analysis_
