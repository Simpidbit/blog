# 导入套接字模块，用于网络通信
import socket
# 导入 threading 模块，用于创建线程
import threading
# 导入 json 模块，用于处理 JSON 格式数据
import json
# 导入 network 模块，很可能是自定义模块，用于网络数据传输
import network
# 导入 copy 模块，用于对象的浅拷贝和深拷贝
import copy
# 导入 platform 模块，用于获取操作系统信息
import platform
# 导入 os 模块，用于操作系统功能，如文件路径和目录操作
import os

# 获取端口号，用于接收客户端的请求
GET_PORT = 9999
# 发送端口号，用于接收客户端发送的文件和目录信息
SEND_PORT = 12555

# 根据操作系统类型确定文件分隔符，用于构建文件路径
if platform.system() == "Windows":
    SEP_SYMBOL = '\\'
else:
    SEP_SYMBOL = '/'

# 定义根目录开始的路径字符串
BEGIN_PATH = f'.{SEP_SYMBOL}root'

# 定义用于存储目录结构信息的 JSON 文件路径
JSON_PATH = f".{SEP_SYMBOL}directory.json"


# 比较两个字典表示的目录结构，找出新文件的路径
def find_newfile_path(origindt, newdt, pathlist):
    # 扫描当前层的origindt和newdt
    """
    找出原始字典和新字典之间的差异，并返回新文件的路径列表。

    参数：
        origindt（字典）：表示原始目录结构的字典。
        newdt（字典）：表示新目录结构的字典。
        pathlist（列表）：当前路径的列表，表示从根目录到当前目录的路径。

    返回：
        列表：新文件的路径列表。

    """

    # 分别获取原始字典和新字典的键集（用于找出差异）
    origin_key_set = set()
    new_key_set = set()
    for key in origindt:
        origin_key_set.add(key)
    for key in newdt:
        new_key_set.add(key)
    # 计算新键集与原始键集的差集（表示新文件或目录）
    compare_set = new_key_set - origin_key_set

    # 如果差集为空，则表示当前层没有差异
    if len(compare_set) == 0:
        # 遍历原始字典的键
        for key in origindt:
            # 如果当前键对应的值表示一个目录
            if origindt[key][1] == 1:
                # 递归地在子字典中查找新文件路径
                ret = find_newfile_path(origindt[key][2], newdt[key][2], copy.deepcopy(pathlist + [key]))
                # 如果递归过后没有找到，则啥事没有
                if ret is None:
                    pass
                # 如果递归找到了新文件路径，则返回该路径
                else:
                    return ret
    # 表示当前层有差异
    else:
        print("判断此层有差异!")
        # 将新字典赋值给 cursor
        cursor = copy.deepcopy(newdt)
        # 从差集里取出新文件或目录的键
        key = compare_set.pop()
        # 循环操作，直到找到新文件的路径或者确定其为目录
        while True:
            # 如果 cursor[key] 对应的值表示一个目录
            if cursor[key][1] == 1:
                # 将键添加到路径列表
                pathlist.append(key)
                # 复制当前 cursor 字典，用于后续查找
                tmp = copy.deepcopy(cursor)
                # 将 cursor 更新为当前目录的子字典
                cursor = cursor[key][2]
                # 取子字典的第一个键，用于下一次循环判断
                key = list(tmp[key][2].keys())[0]
            # 如果 cursor[key] 对应的值表示一个文件
            elif cursor[key][1] == 0:
                # 返回当前路径列表加上文件键，即新文件的完整路径
                return copy.deepcopy(pathlist + [key])


# 在服务器端处理发送(Send)操作，更新目录结构并存储新文件
def send_handler(json_data, fileraw):
    # 打开JSON文件，读取其中的旧数据
    with open(JSON_PATH, "rt") as f:
        old_data = f.read()
    # 将读取的JSON字符串解析为字典
    old_data = json.loads(old_data)
    
    # 通过比较旧数据和新数据，找出新文件的路径
    pathlist = find_newfile_path(old_data, json_data, [])
    
    # 将新数据写入JSON文件，更新目录结构
    with open(JSON_PATH, "wt") as f:
        f.write(json.dumps(json_data))
    
    # 打印找出的新文件路径列表
    print(f"pathlist: {pathlist}")
    # 初始化新的目录结构指针
    new_cursor = json_data
    # 初始化旧的目录结构指针
    old_cursor = old_data
    # 初始化索引值为0，用于遍历pathlist
    index = 0
    
    # 初始化基础路径字符串
    pathstr = BEGIN_PATH
    # 不断循环，直到处理完pathlist中的所有路径
    while True:
        # 打印循环开始时的索引值和当前处理的路径段
        print(f"while开始, index = {index}, pathlist[index] = {pathlist[index]}")
        # 打印循环开始时的pathstr
        print(f"开始时pathstr: {pathstr}")
        # 如果pathlist[index]在旧目录结构指针old_cursor的键中
        if pathlist[index] in old_cursor.keys():
            # 在pathstr末尾添加路径分隔符和当前的路径段
            pathstr += f"{SEP_SYMBOL}{pathlist[index]}"
            # 如果已经处理到pathlist的最后一个元素
            if index == len(pathlist) - 1:
                # 打开对应的文件，将新的文件原始数据写入其中
                with open(pathstr, "wt") as f:
                    f.write(fileraw)
                # 此时所有操作完成，返回
                return
            else:
                # 将old_cursor更新为当前路径对应的子字典，即进入下一层目录
                old_cursor = old_cursor[pathlist[index]][2]
                # 将new_cursor更新为当前路径对应的子字典
                new_cursor = new_cursor[pathlist[index]][2]
                # 索引值加1，处理下一个路径段
                index += 1
        else:
            # 如果pathlist[index]不在旧目录结构指针old_cursor的键中
            if index == len(pathlist) - 1:
                # 则在pathstr末尾添加路径分隔符和当前的路径段，构建新文件的完整路径
                pathstr += f"{SEP_SYMBOL}{pathlist[index]}"
                # 创建新的目录路径，并在其中创建文件
                os.system(f"mkdir {pathstr}")
                # 打开对应的文件，将新的文件原始数据写入其中
                with open(pathstr, "wt") as f:
                    f.write(fileraw)
                # 此时所有操作完成，返回
                return
            else:
                # 在pathstr末尾添加路径分隔符和当前的路径段，构建新目录的完整路径
                pathstr += f"{SEP_SYMBOL}{pathlist[index]}"
                # 创建新的目录路径
                os.system(f"mkdir {pathstr}")
                # 将new_cursor更新为当前路径对应的子字典
                new_cursor = new_cursor[pathlist[index]][2]
                # 索引值加1，处理下一个路径段
                index += 1


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
        conn.send(json.dumps(data).encode("utf-8"))
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
        # 通过自定义的 network 模块接收客户端发送的所有数据
        raw = network.recv_all(conn).decode("utf-8")
        # 关闭与客户端的连接
        conn.close()
        # 关闭套接字
        sock.close()
        
        # 将客户端发送的数据分割成消息头和文件原始数据两部分
        raw_piece = raw.split('\r\nDATA_RAW_SPLIT\r\n')
        # 从消息头中解析出 JSON 格式的目录结构数据
        data = json.loads(raw_piece[0][1:])
        # 文件原始数据
        file_raw = raw_piece[1]
        
        # 根据消息头的第一个字符判断客户端的操作类型，若是 "S" 则为发送新文件
        if raw[0] == "S":
            # 打印客户端发送的目录结构数据
            json_data = data
            print(f"Send: {json_data}")
            # 打印客户端发送的文件原始数据
            print(f"fileraw: {file_raw}")
            # 调用处理发送操作的函数，更新目录结构并存储新文件
            send_handler(json_data, file_raw)
        # 若是 "U" 则为更新已存在文件的内容  
        elif raw[0] == "U":
            # 打印客户端发送的更新操作信息
            pathlist = data
            print(f"Update: {pathlist}")
            # 打印客户端发送的文件更新数据
            print(f"fileraw: {file_raw}")
            # 调用处理更新操作的函数，更新目录中已存在文件的内容
            update_handler(pathlist, file_raw)

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

