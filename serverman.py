import socket
import threading
import json
import network
import copy
import platform
import os

GET_PORT = 9999
SEND_PORT = 12555

if platform.system() == "Windows":
    SEP_SYMBOL = '\\'
else:
    SEP_SYMBOL = '/'


BEGIN_PATH = f'.{SEP_SYMBOL}root'
JS_PATH = f".{SEP_SYMBOL}directory.json"


test_data = {
    "hello.md": ["测试", 0],
    "math": ["数学", 1, {
        "bajian": ["拔尖", 1, {
            "note.md": ["笔记", 0]
        }]
    }],
    "program": ["项目", 1, {
        "blog.md": ["blog开发文档", 0]
    }]
}

test_data2 = {
    "hello.md": ["测试", 0],
    "math": ["数学", 1, {
        "bajian": ["拔尖", 1, {
            "note.md": ["笔记", 0]
        }]
    }],
    "program": ["项目", 1, {
        "blog.md": ["blog开发文档", 0],
        "test.md": ["测试一下", 0]
    }]
}

def find_newfile_path(origindt, newdt, pathlist):

    # 扫描当前层的origindt和newdt
    origin_key_set = set()
    new_key_set = set()
    for key in origindt: origin_key_set.add(key)
    for key in newdt: new_key_set.add(key)
    compare_set = new_key_set - origin_key_set


    if len(compare_set) == 0:       # 此层无差异
        for key in origindt:        # 随便哪一层都行
            if origindt[key][1] == 1:       # dir
                ret = find_newfile_path(origindt[key][2], newdt[key][2], copy.deepcopy(pathlist + [key]))
                if ret is None:
                    pass
                else:
                    return ret
    else:       # 此层有差异
        print("判断此层有差异!")
        cursor = copy.deepcopy(newdt)
        key = compare_set.pop()
        while True:
            if cursor[key][1] == 1:        # 目录
                pathlist.append(key)
                tmp = copy.deepcopy(cursor)
                cursor = cursor[key][2]
                key = list(tmp[key][2].keys())[0]
            elif cursor[key][1] == 0:      # 文件
                return copy.deepcopy(pathlist + [key])


def send_handler(json_data, fileraw):
    with open(JS_PATH, "rt") as f:
        old_data = f.read()
    old_data = json.loads(old_data)
    pathlist = find_newfile_path(old_data, json_data, [])
    with open(JS_PATH, "wt") as f:
        f.write(json.dumps(json_data))

    print(f"pathlist: {pathlist}")
    cursor = json_data
    index = 0
    pathstr = BEGIN_PATH
    while True:
        print(f"while开始, index = {index}, pathlist[index] = {pathlist[index]}")
        print(f"开始时pathstr: {pathstr}")
        if pathlist[index] in cursor.keys():     # 在里面
            pathstr += f"{SEP_SYMBOL}{pathlist[index]}"
            if index == len(pathlist) - 1:
                with open(pathstr, "wt") as f:
                    f.write(fileraw)
                return
            else:
                cursor = cursor[pathlist[index]][2]
                index += 1
        else:       # 不在里面
            if index == len(pathlist) - 1:      # 是最后一位
                pathstr += f"{SEP_SYMBOL}{pathlist[index]}"
                with open(pathstr, "wt") as f:
                    f.write(fileraw)
                return
            else:       # 不是最后一位
                pathstr += f"{SEP_SYMBOL}{pathlist[index]}"
                os.system(f"mkdir {pathstr}")
                cursor = cursor[pathlist[index]][2]
                index += 1


def update_handler(json_data, fileraw):
    pass

def get_server():
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", GET_PORT))
        sock.listen(32)
        conn, addr = sock.accept()
        with open(JS_PATH, "rt") as f:
            data = f.read()
        conn.send(json.dumps(data).encode("utf-8"))
        conn.close()
        sock.close()

def send_server():
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", SEND_PORT))
        sock.listen(32)
        conn, addr = sock.accept()
        raw = network.recv_all(conn).decode("utf-8")
        conn.close()
        sock.close()

        raw_piece = raw.split('\r\nDATA_RAW_SPLIT\r\n')
        data = json.loads(raw_piece[0][1:])
        file_raw = raw_piece[1]
        if raw[0] == "S":           # send
            json_data = data
            print(f"Send: {json_data}")
            print(f"fileraw: {file_raw}")
            send_handler(json_data, file_raw)
        elif raw[0] == "U":         # update
            pathlist = data
            print(f"Update: {pathlist}")
            print(f"fileraw: {file_raw}")
            update_handler(pathlist, file_raw)

if __name__ == '__main__':
    get_th = threading.Thread(target = get_server)
    send_th = threading.Thread(target = send_server)

    send_th.start()
    get_th.start()

    get_th.join()
    send_th.join()
