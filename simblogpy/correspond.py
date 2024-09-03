import socket
import json

from simblogpy.log import print_func_to_log, printlog


HOST = "127.0.0.1"
JSON_PORT = 9999
SEND_PORT = 12555


def send_to_server(msg: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, SEND_PORT))
    sock.send(msg.encode("utf-8"))
    sock.close()


def recv_all__bytes(sock, bufsiz=1024) -> bytes:
    """Receive until no more data."""
    data = b''
    while True:
        part = sock.recv(bufsiz)
        data += part
        if len(part) < bufsiz:
            break
    return data

def get_json_from_server__dict() -> dict:
    """
    Connect to the specified server,
    receive JSON data,
    parse JSON into a dictionary.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, JSON_PORT))
    raw = recv_all__bytes(s).decode("utf-8")
    s.close()
    return json.loads(raw)

"""
Args:
    new_json: dict. JSON after adding new articles/directories.
    file_raw_dict: dict. Key is path of article, and value is its raw.

Message format:
    new_json\r\nDATA_RAW_SPLIT\r\nfile_raw_dict

"""
@print_func_to_log
def add_files_to_server__None(new_json, file_raw_dict):
    """Send new data to server."""
    msgraw = f"S{json.dumps(new_json)}\r\nDATA_RAW_SPLIT\r\n{json.dumps(file_raw_dict)}"
    printlog(f"\t\t\tfile_raw_dict:\n{json.dumps(file_raw_dict)}")
    send_to_server(msgraw)

if __name__ == '__main__':
    pass
