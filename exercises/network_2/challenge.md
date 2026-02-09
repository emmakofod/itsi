# Network Forensics Analysis - cap.pcapng

## Comprehensive Answers with Packet Numbers

---

### Question 1: What is the IP address of demo.testfire.net, and what is Thor's IP address?

**Methodology:**

1. Apply display filter: `dns.qry.name contains "testfire"`
2. Look at DNS response packets (packets 1573, 1576)
3. Check the "Answers" section to see the resolved IP: 65.61.137.117
4. Thor's IP can be seen as the source IP in any outgoing packet or destination in DNS responses

**Answer:**

- **demo.testfire.net IP:** 65.61.137.117
- **Thor's IP:** 192.168.1.125

**Packet References:**

- DNS responses in packets **1573** and **1576** show demo.testfire.net resolves to 65.61.137.117
- Thor's IP (192.168.1.125) appears throughout the traffic as the source address

---

### Question 2: In what package(s) did we get the DNS response, and what happened?

**Methodology:**

1. Apply display filter: `dns.qry.name contains "testfire"`
2. Identify packets with DNS responses (look for packets with "Answers" field populated)
3. Examine packets 1573 and 1576 - these contain DNS A record responses
4. Check the DNS answer section to see the resolved IP address

**Answer:**
DNS responses were received in packets **1573** and **1576**.

**What happened:**

- Thor (192.168.1.125) sent DNS queries for demo.testfire.net
- Packets 1573 and 1576 contained DNS A record responses
- Both responses returned the IP address 65.61.137.117 for demo.testfire.net

**Packet References:**

- Packet **1569**: DNS query for demo.testfire.net
- Packet **1573**: DNS response with IP 65.61.137.117
- Packet **1576**: Additional DNS response with IP 65.61.137.117

---

### Question 3: What kind of service(s) did Thor access on demo.testfire.net?

**Methodology:**

1. Apply display filter: `ip.addr==65.61.137.117 and ip.addr==192.168.1.125`
2. Look for the TCP 3-way handshake (SYN, SYN-ACK, ACK)
3. Check the destination port in the SYN packet (1574) - it's port 80 (HTTP)
4. Confirm by looking at packet 1583 which shows an HTTP GET request
5. Statistics → Conversations → TCP tab can also show port 80 connections

**Answer:**
Thor accessed **HTTP service (port 80)** on demo.testfire.net.

**Packet References:**

- Packet **1574**: TCP SYN to port 80 (initiate connection)
- Packet **1581**: TCP SYN-ACK from port 80 (server accepts)
- Packet **1582**: TCP ACK (connection established)
- Packet **1583**: HTTP GET request for "/" (root page)

**TCP 3-Way Handshake Details:**

- **Packet 1574** (SYN):
  - Source: 192.168.1.125:59557 → Dest: 65.61.137.117:80
  - Flags: SYN
  - Seq: 1188992502 (raw), 0 (relative)

- **Packet 1581** (SYN-ACK):
  - Source: 65.61.137.117:80 → Dest: 192.168.1.125:59557
  - Flags: SYN, ACK
  - Seq: 3775696889 (raw), 0 (relative)
  - Ack: 1188992503 (raw), 1 (relative)

- **Packet 1582** (ACK):
  - Source: 192.168.1.125:59557 → Dest: 65.61.137.117:80
  - Flags: ACK
  - Seq: 1188992503 (raw), 1 (relative)
  - Ack: 3775696890 (raw), 1 (relative)

---

### Question 4: HTTP traffic was observed. Tell what elements the first page accessed contained?

**Methodology:**

1. Apply display filter: `http.request and ip.dst==65.61.137.117`
2. Look at the first HTTP GET request (packet 1583) for "/"
3. Examine subsequent HTTP requests - these are resources loaded by the page
4. List all the URIs requested: CSS files, images, and other resources
5. Alternatively: File → Export Objects → HTTP to see all HTTP objects

**Answer:**
The first page (/) contained the following elements:

**CSS:**

- style.css

**Images:**

- logo.gif
- header_pic.jpg
- pf_lock.gif
- home1.jpg
- home2.jpg
- home3.jpg
- gradient.jpg
- favicon.ico (resulted in 404 error)

**Packet References:**

- Packet **1583**: HTTP GET / (main page request)
- Packet **1611**: HTTP GET /style.css
- Packet **1628**: HTTP GET /images/logo.gif
- Packet **1629**: HTTP GET /images/header_pic.jpg
- Packet **1630**: HTTP GET /images/pf_lock.gif
- Packet **1631**: HTTP GET /images/home1.jpg
- Packet **1632**: HTTP GET /images/home2.jpg
- Packet **1633**: HTTP GET /images/home3.jpg
- Packet **1639**: HTTP GET /images/gradient.jpg
- Packet **1687**: HTTP GET /favicon.ico

---

### Question 5: How did the user land on demo.testfire.net? Any indications on what directed him there?

**Methodology:**

1. Go to packet 1583 (the first HTTP GET request to demo.testfire.net)
2. Expand the HTTP header section
3. Look for the "Referer" field in the HTTP headers
4. The Referer shows the URL the user came from

**Answer:**
The user arrived at demo.testfire.net from **Google Denmark (www.google.dk)**.

**Evidence:**
The HTTP request in packet 1583 contains the Referer header:

```
Referer: https://www.google.dk/
```

This indicates the user clicked a link from a Google Denmark search results page.

**Packet Reference:**

- Packet **1583**: Contains Referer header showing www.google.dk

---

### Question 6: A photo called "home1.jpg" is fetched from demo.testfire.net. Try to extract it

**Methodology:**

1. Apply filter: `http.request.uri contains "home1.jpg"` to find the request (packet 1631)
2. Find the HTTP response with status 200 OK for this request
3. Method 1 - Via browser: Copy the full URI (http://demo.testfire.net/images/home1.jpg) and download via browser
4. Method 2 - Via Wireshark: File → Export Objects → HTTP → find home1.jpg → Save
5. Method 3 - Follow TCP stream: Right-click packet 1631 → Follow → TCP Stream → Show and save data as raw → Save as .jpg

**Answer:**
✓ Successfully extracted home1.jpg

**File Details:**

- Format: JPEG image data, JFIF standard 1.01
- Resolution: 72x72 DPI
- Dimensions: 170x114 pixels
- Size: 7.8 KB

The extracted image has been saved to the outputs folder.

**Packet Reference:**

- Packet **1631**: HTTP GET request for /images/home1.jpg

---

### Question 7: Which packet(s) contains the photo?

**Methodology:**

1. Find the request packet 1631 for home1.jpg
2. Right-click → Follow → TCP Stream
3. Look at the Info column for packets with "[TCP segment of a reassembled PDU]" or JPEG data
4. Alternative: Apply filter `tcp.stream==47 and ip.src==65.61.137.117 and tcp.len>0`
5. Identify packets carrying the JPEG image data (they have TCP payload containing JPEG bytes)

**Answer:**
The home1.jpg photo data is contained in the following packets:

**Response packets containing JPEG data:**

- Packet **1656**: 1380 bytes of JPEG data
- Packet **1658**: 1380 bytes of JPEG data
- Packet **1659**: 1380 bytes of JPEG data
- Packet **1660**: 1380 bytes of JPEG data
- Packet **1681**: 1380 bytes of JPEG data
- Packet **1682**: 1248 bytes of JPEG data (final segment)

**Total:** 6 packets containing the complete JPEG image (~8KB total)

**TCP Stream:** Stream 47

---

### Question 8: How many HTTP requests were in total made to demo.testfire.net?

**Methodology:**

1. Apply display filter: `http.request and ip.dst==65.61.137.117`
2. Count the number of packets displayed
3. Alternative: Statistics → HTTP → Requests → filter by host "demo.testfire.net"
4. Check each packet's HTTP Request URI field

**Answer:**
**10 HTTP requests** were made to demo.testfire.net.

**Complete list:**

| Packet | Method | URI                    |
| ------ | ------ | ---------------------- |
| 1583   | GET    | /                      |
| 1611   | GET    | /style.css             |
| 1628   | GET    | /images/logo.gif       |
| 1629   | GET    | /images/header_pic.jpg |
| 1630   | GET    | /images/pf_lock.gif    |
| 1631   | GET    | /images/home1.jpg      |
| 1632   | GET    | /images/home2.jpg      |
| 1633   | GET    | /images/home3.jpg      |
| 1639   | GET    | /images/gradient.jpg   |
| 1687   | GET    | /favicon.ico           |

---

### Question 9: What is going on in packet 1694, and to what is that packet replying?

**Methodology:**

1. Go to packet 1694
2. Look at the Info column - shows "HTTP/1.1 404 Not Found"
3. Expand the HTTP protocol section
4. Check the "Response Code" field (404)
5. Look for "[Request in frame: X]" in the HTTP section to see which request this is responding to
6. Examine packet 1687 to see what was requested

**Answer:**
Packet **1694** contains an **HTTP/1.1 404 Not Found** response.

**What's happening:**

- The server (demo.testfire.net) is responding that the requested file was not found
- This is replying to the request in packet **1687** for /favicon.ico
- The browser automatically requested a favicon, but the file doesn't exist on the server

**Details:**

- Status Code: 404
- Status Text: Not Found
- Server: Microsoft-IIS/8.0
- Content-Length: 1245 bytes (HTML error page)
- Request it's replying to: Packet **1687** (GET /favicon.ico)

**Packet References:**

- Packet **1687**: HTTP GET request for /favicon.ico
- Packet **1694**: HTTP 404 Not Found response

---

### Question 10: TCP connection with demo.testfire.net torn down? If yes then where, and if no then why not?

**Methodology:**

1. Apply filter: `ip.addr==65.61.137.117 and ip.addr==192.168.1.125 and tcp.flags.fin==1`
2. Look for FIN packets (connection teardown initiation)
3. If no FIN packets found, apply filter: `ip.addr==65.61.137.117 and tcp.analysis.keep_alive`
4. Look for TCP Keep-Alive packets (indicated by "[TCP Keep-Alive]" in Info column)
5. Scroll to end of capture to see if connections are still maintained

**Answer:**
**No, the TCP connections were NOT torn down.**

**Why not:**
The connections used **HTTP Keep-Alive** to maintain persistent connections. Instead of closing the connection after each request/response, the connections remained open for potential reuse.

**Evidence:**

- No FIN (finish) packets were found in the traffic between Thor and demo.testfire.net
- TCP Keep-Alive packets are present throughout the capture
- Keep-alive packets observed in frames: 1793-1806, 1887-1899, 1936-1952, 2047-2063

**Significance:**
HTTP/1.1 uses persistent connections by default to improve performance by avoiding the overhead of establishing new TCP connections for each HTTP request. The connections remained open at the end of the capture.

---

### Question 11: Figure out who is behind the IP address 172.217.19.195 (without using Google)

**Methodology:**

1. Apply display filter: `dns.a==172.217.19.195`
2. Look at DNS response packets that resolved to this IP
3. Check the "Queries" section to see what domain name was queried
4. The domain name will indicate the owner/service

**Answer:**
The IP address **172.217.19.195** belongs to **Google** (specifically, Google Denmark servers).

**Evidence from DNS:**
DNS responses show that the following domains resolve to 172.217.19.195:

- **www.google.dk** (Google Denmark)
- **www.gstatic.com** (Google's static content delivery network)

**Packet References:**

- Packet **884**: DNS response showing www.google.dk → 172.217.19.195
- Packet **1209**: DNS response showing www.gstatic.com → 172.217.19.195
- Packet **1211**: Another DNS response for www.gstatic.com → 172.217.19.195

---

### Question 12: A machine has the IP address 192.168.1.101. Try to find its hostname

**Methodology:**

1. Apply filter: `ip.addr==192.168.1.101`
2. Look for DHCP packets (BOOTP protocol)
3. Find a DHCP Request or DHCP Inform packet from this IP
4. Expand the "Bootstrap Protocol" section
5. Look for "Option: (12) Host Name" field
6. Alternative: Look for NetBIOS Name Service packets or mDNS queries from this IP

**Answer:**
The hostname for IP **192.168.1.101** is **DanyiPad**.

**Evidence:**

- DHCP Option 12 (Host Name) contains "DanyiPad"
- MAC Address: a4:67:06:8d:83:a1 (Apple Inc. device)
- Device type: iPad (based on hostname and Apple MAC address)

**How found:**
The hostname was discovered in DHCP traffic where the device announced its hostname to the network.

---

### Question 13: Generate a list of all the endpoints (IPv4) seen on the network

**Methodology:**

1. Go to Statistics → Endpoints
2. Select the IPv4 tab
3. This shows all unique IPv4 addresses in the capture
4. Alternative: Statistics → Conversations → IPv4 tab
5. Export or manually list the IP addresses
6. Filter out special addresses like 0.0.0.0, multicast (224.x.x.x), and broadcast (255.255.255.255) if needed

**Answer:**

**Local Network (192.168.1.x):**

- 192.168.1.1 (likely gateway/router)
- 192.168.1.3
- 192.168.1.40
- 192.168.1.101 (DanyiPad)
- 192.168.1.102
- 192.168.1.107
- 192.168.1.109
- 192.168.1.111
- 192.168.1.123
- 192.168.1.125 (Thor - the machine being analyzed)
- 192.168.1.128
- 192.168.1.136
- 192.168.1.146
- 192.168.1.254

**External Internet IPs:**

_Google Services (172.217.x.x, 108.177.x.x, 216.58.x.x, 173.194.x.x):_

- 108.177.96.188
- 108.177.119.189
- 172.217.17.97
- 172.217.17.98
- 172.217.17.129
- 172.217.19.195 (www.google.dk)
- 172.217.19.206
- 172.217.20.66
- 172.217.20.99
- 172.217.20.100
- 172.217.20.109
- 172.217.28.195
- 173.194.69.189
- 216.58.211.99
- 216.58.212.132
- 216.58.212.174

_Microsoft Services:_

- 40.77.229.41
- 52.164.227.208

_Other Services:_

- 54.235.105.11
- 65.61.137.117 (demo.testfire.net)
- 66.135.202.233
- 92.122.173.194
- 94.18.243.147
- 151.101.36.207
- 162.125.18.133
- 162.125.34.129
- 162.125.34.137
- 162.254.193.46
- 198.252.206.25

**Multicast/Broadcast Addresses:**

- 224.0.0.2 (All routers)
- 224.0.0.7 (RIP)
- 224.0.0.251 (mDNS)
- 224.0.0.252 (LLMNR)
- 224.0.0.253 (NTP)
- 224.0.1.60 (Unknown)
- 239.255.3.22 (Organization-Local Scope)
- 239.255.255.246 (Organization-Local Scope)
- 239.255.255.250 (SSDP)

**Special Addresses:**

- 0.0.0.0 (Unspecified address)
- 255.255.255.255 (Broadcast)

**Total unique IPv4 endpoints:** 56 addresses

---

## Summary

This network capture shows Thor (192.168.1.125) visiting demo.testfire.net after arriving from a Google Denmark search. The session involved 10 HTTP requests to fetch the homepage and its resources including images and CSS. The TCP connections remained open using HTTP keep-alive, and no explicit connection teardown was observed. The network also shows significant Google service traffic and various local network devices including an iPad named "DanyiPad".
