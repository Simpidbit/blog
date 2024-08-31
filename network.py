import socket
import json

HOST = "127.0.0.1"
GET_PORT = 9999
SEND_PORT = 12555

def recv_all(sock, bufsiz=1024) -> bytes:
    """
    持续接收数据，直到没有更多数据可接收为止。

    参数：
    sock：套接字对象。
    bufsiz（可选）：接收缓冲区大小。默认为1024字节。

    返回：
    bytes：接收的所有数据。
    """
    data = b''
    while True:
        part = sock.recv(bufsiz)
        data += part
        if len(part) < bufsiz:
            break
    return data

def get_json_from_server() -> dict:
    """
    连接到指定的服务器，接收 JSON 格式数据，并将其解码为字典。

    返回：
    dict：从服务器接收的 JSON 数据。
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, GET_PORT))
    raw = recv_all(s).decode("utf-8")
    s.close()
    return json.loads(raw)

def send_add(json_data, filepath):
    """
    将 JSON 数据和文件内容发送到指定服务器的特定端口。

    参数：
    json_data：要发送的 JSON 数据。
    filepath：要发送的文件路径。
    """
    with open(filepath, "rt") as f:
        raw = f.read()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, SEND_PORT))
    sock.send((f"S{json.dumps(json_data)}\r\nDATA_RAW_SPLIT\r\n{raw}".encode("utf-8")))
    sock.close()

def update_add(pathlist, filepath):
    """
    将路径列表的 JSON 表示和文件内容发送到指定服务器的特定端口。

    参数：
    pathlist：路径列表，转换为 JSON 发送。
    filepath：要发送的文件路径。
    """
    with open(filepath, "rt") as f:
        raw = f.read()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, SEND_PORT))
    sock.send(f"U{json.dumps(pathlist)}\r\nDATA_RAW_SPLIT\r\n{raw}".encode("utf-8"))
    sock.close()

