import socket
import json

HOST = "127.0.0.1"
GET_PORT = 9999
SEND_PORT = 12555

def recv_all(sock, bufsiz = 1024) -> bytes:
    data = b''
    while True:
        part = sock.recv(bufsiz)
        data += part
        if len(part) < bufsiz:
            break
    return data

def get_json_from_server() -> dict:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, GET_PORT))
    raw = recv_all(s).decode("utf-8")
    s.close()
    return json.loads(raw)

def send_add(json_data, filepath):
    with open(filepath, "rt") as f:
        raw = f.read()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, SEND_PORT))
    sock.send((f"S{json.dumps(json_data)}\r\nDATA_RAW_SPLIT\r\n{raw}".encode("utf-8")))
    sock.close()

def update_add(pathlist, filepath):
    with open(filepath, "rt") as f:
        raw = f.read()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, SEND_PORT))
    sock.send(f"U{json.dumps(pathlist)}\r\nDATA_RAW_SPLIT\r\n{raw}".encode("utf-8"))
    sock.close()
