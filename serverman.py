import socket
import threading
import json
import copy
import os

from simblogpy.filejson import scan_file_json_to_path, get_file_dir__str
from simblogpy.string import SEP_SYMBOL
from simblogpy import correspond
from simblogpy.log import print_to_log

GET_PORT = 9999
SEND_PORT = 12555


BEGIN_PATH = f'.{SEP_SYMBOL}root'
JSON_PATH = f".{SEP_SYMBOL}directory.json"


"""
old_pathlists or new_pathlists: [ ["filepath", 0 or 1(filetype)], ... ]
"""
@print_to_log
def diff_between_old_new__list(old_pathlists, new_pathlists):
    """Return what new_pathlists has but old_pathlists doesn't."""
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
    scan_file_json_to_path(old_data, [], old_pathlists)
    scan_file_json_to_path(json_data, [], new_pathlists)

    compare_pathlists = diff_between_old_new__list(old_pathlists, new_pathlists)
    print(f"old_pathlists: {old_pathlists}")
    print(f"new_pathlists: {new_pathlists}")
    print("compare_pathlists", compare_pathlists)
    for eachpath in compare_pathlists:

        # 打通路径
        if eachpath[1] == 0:
            try:
                print(f"正在尝试打通路径: {BEGIN_PATH}{get_file_dir__str(eachpath[0])}")
                os.makedirs(BEGIN_PATH + get_file_dir__str(eachpath[0]))
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
    # 读取 JSON 文件中的旧目录结构信息
    with open(JSON_PATH, "rt") as f:
        old_data = f.read()
    # 将 JSON 字符串转换为 Python 对象（字典）
    old_data = json.loads(old_data)
    
    # 游标，用于在目录结构中导航
    cursor = old_data
    # 索引，用于遍历 pathlist
    index = 0
    # 初始化路径字符串，用于构建文件的完整路径
    pathstr = ""
    # 遍历 pathlist 中的路径片段，直到最后一个片段（文件名）
    for key in pathlist[:-1]:
        # 将每个路径片段添加到路径字符串中，形成完整的目录路径
        pathstr += f"{SEP_SYMBOL}{key}"
        # 在目录结构中导航到当前路径的父目录
        cursor = cursor[key][2]
    
    # 获取文件名，即 pathlist 中的最后一个元素
    filename = pathlist[-1]
    # 使用完整路径打开文件，并将更新的内容写入文件
    with open(f"{BEGIN_PATH}{pathstr}{SEP_SYMBOL}{filename}", "wt") as f:
        f.write(fileraw)


# 获取目录结构的 JSON 数据的服务器端处理函数
def get_json_server():
    # 无限循环，持续监听客户端的连接请求
    while True:
        # 创建 TCP 套接字，用于接收客户端连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 将套接字绑定到指定的 IP 地址和端口，这里是服务器的 IP 和 GET_PORT
        sock.bind(("0.0.0.0", GET_PORT))
        # 开始监听端口，允许最多 32 个客户端同时连接
        sock.listen(32)
        # 等待客户端连接，accept() 函数会阻塞直到有客户端连接
        conn, addr = sock.accept()
        # 打开 JSON 文件，读取目录结构数据
        with open(JSON_PATH, "rt") as f:
            # 读取文件内容
            data = f.read()
        # 将目录结构数据编码为字节流，并发送给客户端
        conn.send(data.encode("utf-8"))
        # 关闭与客户端的连接
        conn.close()
        # 关闭套接字
        sock.close()


# 发送文件的服务器端处理函数，主要处理客户端发送来的文件和目录信息
def send_file_server():
    # 无限循环，持续监听客户端的连接请求
    while True:
        # 创建 TCP 套接字，用于接收客户端连接
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 将套接字绑定到指定的 IP 地址和端口，这里是服务器的 IP 和 SEND_PORT
        sock.bind(("0.0.0.0", SEND_PORT))
        # 开始监听端口，允许最多 32 个客户端同时连接
        sock.listen(32)
        # 等待客户端连接，accept() 函数会阻塞直到有客户端连接
        conn, addr = sock.accept()
        # 通过自定义的 correspond 模块接收客户端发送的所有数据
        raw = correspond.recv_all__bytes(conn).decode("utf-8")
        # 关闭与客户端的连接
        conn.close()
        # 关闭套接字
        sock.close()
        
        # 将客户端发送的数据分割成消息头和文件原始数据两部分
        raw_piece = raw.split('\r\nDATA_RAW_SPLIT\r\n')
        # 从消息头中解析出 JSON 格式的目录结构数据
        print(raw_piece)
        data = json.loads(raw_piece[0][1:])
        # 文件原始数据
        file_raw_data = raw_piece[1]
        
        # 根据消息头的第一个字符判断客户端的操作类型，若是 "S" 则为发送新文件
        if raw[0] == "S":
            # 打印客户端发送的目录结构数据
            json_data = data
            print(f"Send: {json_data}")
            file_raw_json = json.loads(file_raw_data)
            print(f"file_raw_json: {file_raw_json}")
            send_handler(json_data, file_raw_json)
        # 若是 "U" 则为更新已存在文件的内容  
        elif raw[0] == "U":
            # 打印客户端发送的更新操作信息
            pathlist = data
            print(f"Update: {pathlist}")
            # 打印客户端发送的文件更新数据
            print(f"fileraw: {file_raw}")
            # 调用处理更新操作的函数，更新目录中已存在文件的内容
            update_handler(pathlist, file_raw_data)

if __name__ == '__main__':
    # 创建线程，目标函数是 get_json_server()，即启动一个服务器，用于响应客户端获取目录结构 JSON 数据的请求
    get_th = threading.Thread(target=get_json_server)
    # 创建线程，目标函数是 send_file_server()，即启动一个服务器，用于接收客户端发送的文件和目录信息，以便更新服务器目录结构
    send_th = threading.Thread(target=send_file_server)
    
    # 启动 get_json_server() 线程    
    get_th.start()
    # 启动 send_file_server() 线程    
    send_th.start()
    
    # 等待 get_json_server() 线程执行完毕
    get_th.join()
    # 等待 send_file_server() 线程执行完毕
    send_th.join()

