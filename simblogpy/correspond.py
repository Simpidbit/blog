import socket
import json

from simblogpy.log import print_func_to_log, printlog


HOST = "127.0.0.1"
JSON_PORT = 9999
SEND_PORT = 12555

def recv_all__bytes(sock, bufsiz=1024) -> bytes:
    """Receive until no more data."""
    data = b''
    while True:
        part = sock.recv(bufsiz)
        data += part
        if len(part) < bufsiz:
            break
    return data

if __name__ == '__main__':
    pass
