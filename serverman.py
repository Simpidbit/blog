import socket
import threading
import json
import copy
import os
import platform


GET_PORT = 10001
SEND_PORT = 12555

SEP_SYMBOL = '\\' if platform.system() == "Windows" else "/"

BEGIN_PATH = f'.{SEP_SYMBOL}root'
JSON_PATH = f".{SEP_SYMBOL}directory.json"

def build_pathstr_from_list__local_str(pathlist):
    pathstr = ""
    for each in pathlist:
        pathstr += f"{SEP_SYMBOL}{each}"
    return pathstr

def get_file_dir__local_str(filepath) -> str:
    """Get the directory path where the file is located."""
    path = filepath
    while True:
        path = path[:-1]
        if len(path) == 0:
            break
        if path[-1] == SEP_SYMBOL:
            break
    if len(path) != 0:
        path = path[:-1]
    return path

def scan_file_json_to_path__local_list(data, curlist, paths) -> list:
    for key in data:
        if data[key][1] == 1:
            if len(data[key][2].keys()) == 0:
                paths.append([build_pathstr_from_list__local_str(curlist + [key]), data[key][1]])
            else:
                scan_file_json_to_path__local_list(data[key][2], copy.deepcopy(curlist + [key]), paths)
        else:
            paths.append([build_pathstr_from_list__local_str(curlist + [key]), data[key][1]])

def recv_all__local_bytes(sock, bufsiz=1024) -> bytes:
    """Receive until no more data."""
    data = b''
    while True:
        part = sock.recv(bufsiz)
        data += part
        if len(part) < bufsiz:
            break
    return data


def diff_between_old_new__list(old_pathlists, new_pathlists):
    """
    Return what new_pathlists has but old_pathlists doesn't.

    old_pathlists or new_pathlists: [ ["filepath", 0 or 1(filetype)], ... ]
    """
    compare = []
    for each in new_pathlists:
        if each in old_pathlists:
            pass
        else:
            compare.append(each)
    return compare


# 在服务器端处理发送(Send)操作，更新目录结构并存储新文件
"""
    json_data: 客户端发来的新数据
    filerawdict: key值是文件的path，value是文件raw

"""
def send_handler(json_data, filerawdict):
    # 打开JSON文件，读取其中的旧数据
    with open(JSON_PATH, "rt") as f:
        old_data = f.read()

    # 将新数据写入JSON文件，更新目录结构
    with open(JSON_PATH, "wt") as f:
        f.write(json.dumps(json_data))

    # 将读取的JSON字符串解析为字典
    old_data = json.loads(old_data)
    
    # 通过比较旧数据和新数据，找出新文件的路径
    old_pathlists = []
    new_pathlists = []
    scan_file_json_to_path__local_list(old_data, [], old_pathlists)
    scan_file_json_to_path__local_list(json_data, [], new_pathlists)

    compare_pathlists = diff_between_old_new__list(old_pathlists, new_pathlists)
    print(f"old_pathlists: {old_pathlists}")
    print(f"new_pathlists: {new_pathlists}")
    print("compare_pathlists", compare_pathlists)
    for eachpath in compare_pathlists:

        # 打通路径
        if eachpath[1] == 0:
            try:
                print(f"正在尝试打通路径: {BEGIN_PATH}{get_file_dir__local_str(eachpath[0])}")
                os.makedirs(BEGIN_PATH + get_file_dir__local_str(eachpath[0]))
                print("打通路径成功！")
            except FileExistsError:
                print("打通路径失败，路径已存在")
        elif eachpath[1] == 1:
            try:
                print(f"正在尝试创建目录: {BEGIN_PATH}{eachpath[0]}")
                os.makedirs(f"{BEGIN_PATH}{eachpath[0]}")
                print("创建目录成功！")
            except FileExistsError:
                print("创建目录失败，目录已存在")
            continue

        if eachpath[1] == 0:
            # 写入文件
            with open(f"{BEGIN_PATH}{eachpath[0]}", "wt") as f:
                f.write(filerawdict[eachpath[0]])
        elif eachpath[1] == 1:
            try:
                print(f"正在尝试锚定路径: {eachpath[0]}")
                os.makedirs(f"{BEGIN_PATH}{eachpath[0]}")
                print("锚定路径成功！")
            except FileExistsError:
                print("锚定路径失败，路径已存在")

    

# 在服务器端处理更新(Update)操作，更新目录中已存在文件的内容
def update_handler(pathlist, fileraw):
    """
    处理客户端发来的更新请求，更新目录结构中已存在文件的内容

    参数：
        pathlist（列表）：文件路径的列表，表示要更新的文件在目录结构中的位置
        fileraw（字符串）：更新的文件内容

    返回：
        无

    """
    with open(JSON_PATH, "rt") as f:
        old_data = f.read()
    old_data = json.loads(old_data)
    
    cursor = old_data
    index = 0
    pathstr = ""
    for key in pathlist[:-1]:
        pathstr += f"{SEP_SYMBOL}{key}"
        cursor = cursor[key][2]
    
    filename = pathlist[-1]
    with open(f"{BEGIN_PATH}{pathstr}{SEP_SYMBOL}{filename}", "wt") as f:
        f.write(fileraw)



def remove_handler(json_data, filepath_list):
    # 打开JSON文件，读取其中的旧数据
    old_data = None
    with open(JSON_PATH, "rt") as f:
        old_data = f.read()
        # 将读取的JSON字符串解析为字典
        old_data = json.loads(old_data)

    # 将新数据写入JSON文件，更新目录结构
    with open(JSON_PATH, "wt") as f:
        f.write(json.dumps(json_data))

    # 删除文件/目录
    for filepath in filepath_list:
        os.system(f"rm -r {BEGIN_PATH}{filepath}")



# 获取目录结构的 JSON 数据的服务器端处理函数
def get_json_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", GET_PORT))
    sock.listen(32)
    while True:
        conn, addr = sock.accept()
        with open(JSON_PATH, "rt") as f:
            data = f.read()
        conn.send(data.encode("utf-8"))
        conn.close()
    sock.close()


# 发送文件的服务器端处理函数，主要处理客户端发送来的文件和目录信息
def send_file_server():
    # 无限循环，持续监听客户端的连接请求
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", SEND_PORT))
    sock.listen(32)
    while True:
        conn, addr = sock.accept()
        raw = recv_all__local_bytes(conn).decode("utf-8")
        conn.close()
        
        # 将客户端发送的数据分割成消息头和数据两部分
        raw_piece = raw.split('\r\nDATA_RAW_SPLIT\r\n')
        print("raw_piece[0]:", raw_piece[0])
        print("raw_piece[1]:", raw_piece[1])

        data = raw_piece[1]

        # 根据消息头的第一个字符判断客户端的操作类型，若是 "S" 则为发送新文件
        match raw[0]:
            case 'S':
                # 从消息头中解析出 JSON 格式的目录结构数据
                json_data = json.loads(raw_piece[0][1:])

                print(f"Send: {json_data}")
                file_raw_json = json.loads(data)
                print(f"file_raw_json: {file_raw_json}")
                send_handler(json_data, file_raw_json)

            case 'U':
                # 若是 "U" 则为更新已存在文件的内容  
                pathlist = data
                print(f"Update: {pathlist}")
                print(f"fileraw: {file_raw}")
                # 调用处理更新操作的函数，更新目录中已存在文件的内容
                update_handler(pathlist, file_raw_data)

            case 'G':
                # 下载文件

            case 'R':
                pass

            case 'D':
                # 删除文件或目录
                json_data = json.loads(raw_piece[0][1:])
                remove_handler(json_data, data.split('$$$'))

            case _:
                pass
    sock.close()

if __name__ == '__main__':
    get_th = threading.Thread(target=get_json_server)
    send_th = threading.Thread(target=send_file_server)
    
    get_th.start()
    send_th.start()
    
    get_th.join()
    send_th.join()
