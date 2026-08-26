import socket
import threading

HOST = '0.0.0.0'
TCP_PORT = 5000

# rooms = { room_name: { addr: (conn, udp_port, username) } }
rooms      = {}
rooms_lock = threading.Lock()


def send_ctrl(conn, text):
    data = text.encode()
    conn.sendall(b'\x01' + len(data).to_bytes(2, 'big') + data)

def broadcast_ctrl(room_name, text, skip_addr):
    with rooms_lock:
        targets = [c for a, (c, _, _) in rooms.get(room_name, {}).items() if a != skip_addr]
    for c in targets:
        try:
            send_ctrl(c, text)
        except:
            pass

def broadcast_data(room_name, raw, skip_addr):
    frame = b'\x02' + len(raw).to_bytes(2, 'big') + raw
    with rooms_lock:
        targets = [c for a, (c, _, _) in rooms.get(room_name, {}).items() if a != skip_addr]
    for c in targets:
        try:
            c.sendall(frame)
        except:
            pass

def recv_all(conn, n):
    buf = b''
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError
        buf += chunk
    return buf


def handle_client(conn, addr):
    try:
        # Step 1: send available rooms
        with rooms_lock:
            room_list = list(rooms.keys())
        send_ctrl(conn, "ROOMS " + ",".join(room_list) if room_list else "ROOMS")

        # Step 2: receive CREATE or JOIN
        typ    = conn.recv(1)
        length = int.from_bytes(recv_all(conn, 2), 'big')
        msg    = recv_all(conn, length).decode()
        # msg = "CREATE roomname udp_port username"
        #    or "JOIN   roomname udp_port username"
        parts      = msg.split("|")
        action     = parts[0]          # CREATE or JOIN
        room_name  = parts[1]
        udp_port   = int(parts[2])
        username   = parts[3]
    except Exception as e:
        print(f"[!] Handshake failed {addr}: {e}")
        conn.close()
        return

    print(f"[+] {addr} {action} '{room_name}' UDP:{udp_port} user:{username}")

    with rooms_lock:
        if action == "CREATE":
            if room_name in rooms:
                send_ctrl(conn, "ERR Room already exists")
                conn.close()
                return
            rooms[room_name] = {}
        elif action == "JOIN":
            if room_name not in rooms:
                send_ctrl(conn, "ERR Room not found")
                conn.close()
                return
        rooms[room_name][addr] = (conn, udp_port, username)

    # Send existing peers in room to new client
    with rooms_lock:
        others = [(a, u, n) for a, (_, u, n) in rooms[room_name].items() if a != addr]
    for a, u, n in others:
        send_ctrl(conn, f"PEER {a[0]} {u} {n}")
    send_ctrl(conn, f"ROOMNAME {room_name}")
    send_ctrl(conn, "READY")

    broadcast_ctrl(room_name, f"JOIN {username}", addr)
    broadcast_ctrl(room_name, f"PEER {addr[0]} {udp_port} {username}", addr)

    # Main loop
    while True:
        try:
            typ = conn.recv(1)
            if not typ:
                break
            length = int.from_bytes(recv_all(conn, 2), 'big')
            payload = recv_all(conn, length)
            if typ == b'\x02':
                broadcast_data(room_name, payload, addr)
        except:
            break

    conn.close()
    with rooms_lock:
        if room_name in rooms:
            rooms[room_name].pop(addr, None)
            if not rooms[room_name]:
                del rooms[room_name]
                print(f"[*] Room '{room_name}' closed (empty)")
    broadcast_ctrl(room_name, f"LEFT {username}", addr)
    print(f"[-] {addr} ({username}) left '{room_name}'")


tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_sock.bind((HOST, TCP_PORT))
tcp_sock.listen(10)
print(f"[*] Chat server on :{TCP_PORT}")

while True:
    conn, addr = tcp_sock.accept()
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()