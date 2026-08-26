import socket
import threading
import os
import time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# ── ANSI colours ──────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
WHITE  = "\033[97m"
GREEN  = "\033[92m"

USER_COLORS = ["\033[92m", "\033[94m", "\033[95m", "\033[91m", "\033[93m", "\033[96m"]
color_map, color_index, color_lock = {}, 0, threading.Lock()

def get_color(name):
    global color_index
    with color_lock:
        if name not in color_map:
            color_map[name] = USER_COLORS[color_index % len(USER_COLORS)]
            color_index += 1
        return color_map[name]

def info(msg):    print(f"\n{DIM}{YELLOW}> {msg}{RESET}")
def system(msg):  print(f"\n{DIM}  {msg}{RESET}")

def print_header(room_name):
    w = 44
    print(f"\n{CYAN}{'─' * w}")
    title = f"  ☰  {room_name}"
    print(f"{BOLD}{title:<{w}}{RESET}{CYAN}")
    print(f"{'─' * w}{RESET}\n")

# ── Framing ───────────────────────────────────────────────────────────────────
def send_ctrl(sock, text):
    data = text.encode()
    sock.sendall(b'\x01' + len(data).to_bytes(2, 'big') + data)

def send_data(sock, raw):
    sock.sendall(b'\x02' + len(raw).to_bytes(2, 'big') + raw)

def recv_all(sock, n):
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError
        buf += chunk
    return buf

# ── Setup ─────────────────────────────────────────────────────────────────────
TCP_PORT = 5000

udp_sock_init = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock_init.bind(("", 0))
udp_port = udp_sock_init.getsockname()[1]

server_ip = input(f"{CYAN}Server IP: {RESET}").strip()
username  = input(f"{CYAN}Username: {RESET}").strip()

my_rsa = rsa.generate_private_key(public_exponent=65537, key_size=2048)
my_pub = my_rsa.public_key().public_bytes(
    serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)

aes_key, aesgcm, key_lock     = None, None, threading.Lock()
known_peers, peers_lock        = {}, threading.Lock()


def send_aes_key_to(peer_ip, peer_udp, pub):
    with key_lock:
        k = aes_key
    if not k:
        return
    enc = pub.encrypt(k, padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(enc, (peer_ip, peer_udp))
    s.close()

def udp_thread():
    global aes_key, aesgcm
    udp = udp_sock_init
    while True:
        data, addr = udp.recvfrom(4096)
        if data.startswith(b"-----BEGIN PUBLIC KEY-----"):
            pub = serialization.load_pem_public_key(data)
            with peers_lock:
                reg = known_peers.get(addr[0])
            if reg:
                send_aes_key_to(addr[0], reg, pub)
        else:
            with key_lock:
                if aes_key:
                    continue
            try:
                k = my_rsa.decrypt(data, padding.OAEP(
                    mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
                with key_lock:
                    aes_key = k
                    aesgcm  = AESGCM(k)
                system("secure channel established (E2E)")
            except:
                pass

def request_key_from(peer_ip, peer_udp):
    with peers_lock:
        known_peers[peer_ip] = peer_udp
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(my_pub, (peer_ip, peer_udp))
    s.close()

def handle_ctrl(line):
    if line.startswith("PEER "):
        parts = line.split(" ", 3)
        ip, port, peer_name = parts[1], int(parts[2]), parts[3]
        get_color(peer_name)
        request_key_from(ip, port)
    elif line.startswith("JOIN "):
        peer_name = line[5:]
        c = get_color(peer_name)
        info(f"{c}{BOLD}{peer_name}{RESET}{DIM}{YELLOW} just entered the chat")
    elif line.startswith("LEFT "):
        peer_name = line[5:]
        c = get_color(peer_name)
        info(f"{c}{BOLD}{peer_name}{RESET}{DIM}{YELLOW} left the chat")


# ── Connect ───────────────────────────────────────────────────────────────────
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.connect((server_ip, TCP_PORT))

# Receive room list
typ    = recv_all(tcp_sock, 1)
length = int.from_bytes(recv_all(tcp_sock, 2), 'big')
rooms_msg = recv_all(tcp_sock, length).decode()  # "ROOMS name1,name2" or "ROOMS"

existing_rooms = []
if rooms_msg != "ROOMS" and rooms_msg.startswith("ROOMS "):
    existing_rooms = rooms_msg[6:].split(",")

print()
if existing_rooms:
    print(f"{CYAN}Available rooms:{RESET}")
    for i, r in enumerate(existing_rooms, 1):
        print(f"  {DIM}{i}.{RESET} {WHITE}{r}{RESET}")
    print(f"\n{DIM}  (c) create new room{RESET}")
    choice = input(f"\n{CYAN}Enter number to join, or (c) to create: {RESET}").strip()
    if choice.lower() == "c" or choice == "":
        action    = "CREATE"
        room_name = input(f"{CYAN}Room name: {RESET}").strip()
    else:
        try:
            idx = int(choice) - 1
            room_name = existing_rooms[idx]
        except (ValueError, IndexError):
            room_name = choice   # fallback: typed name directly
        action = "JOIN"
else:
    print(f"{DIM}  no existing rooms — creating one{RESET}")
    room_name = input(f"{CYAN}Room name: {RESET}").strip()
    action    = "CREATE"

print()
send_ctrl(tcp_sock, f"{action}|{room_name}|{udp_port}|{username}")

threading.Thread(target=udp_thread, daemon=True).start()

# Handshake — read until READY
room_confirmed = room_name
while True:
    typ    = recv_all(tcp_sock, 1)
    length = int.from_bytes(recv_all(tcp_sock, 2), 'big')
    payload = recv_all(tcp_sock, length).decode()
    if payload == "READY":
        break
    elif payload.startswith("ERR "):
        print(f"\n{YELLOW}[!] {payload[4:]}{RESET}")
        tcp_sock.close()
        exit(1)
    elif payload.startswith("ROOMNAME "):
        room_confirmed = payload[9:]
    else:
        handle_ctrl(payload)

time.sleep(0.5)
with key_lock:
    if aes_key is None:
        aes_key = os.urandom(32)
        aesgcm  = AESGCM(aes_key)
        system("secure channel established (E2E)")

print_header(room_confirmed)
print(f"{DIM}  connected as {BOLD}{WHITE}{username}{RESET}\n")


def tcp_recv():
    while True:
        try:
            typ     = recv_all(tcp_sock, 1)
            length  = int.from_bytes(recv_all(tcp_sock, 2), 'big')
            payload = recv_all(tcp_sock, length)
            if typ == b'\x01':
                handle_ctrl(payload.decode())
            elif typ == b'\x02':
                with key_lock:
                    gcm = aesgcm
                if gcm:
                    try:
                        pt = gcm.decrypt(payload[:12], payload[12:], None)
                        text = pt.decode()
                        if ": " in text:
                            sender, msg = text.split(": ", 1)
                            c = get_color(sender)
                            print(f"\n{c}{BOLD}{sender}{RESET}: {WHITE}{msg}{RESET}\n")
                        else:
                            print(f"\n{WHITE}{text}{RESET}")
                    except:
                        pass
        except:
            break

threading.Thread(target=tcp_recv, daemon=True).start()

while True:
    msg = input()
    with key_lock:
        gcm = aesgcm
    if not gcm:
        system("waiting for secure channel...")
        continue
    print(f"\033[1A\033[2K{DIM}you{RESET}: {WHITE}{msg}{RESET}\n")
    nonce = os.urandom(12)
    ct    = gcm.encrypt(nonce, f"{username}: {msg}".encode(), None)
    send_data(tcp_sock, nonce + ct)