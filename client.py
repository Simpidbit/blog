"""
摘要：
    有以下若干功能：
        1. 新增文章
        2. 更新已存在的文章
            一种方式：
                从服务器获取原文章，修改后提交至服务器
            另一种方式：
                提交本地文章并覆盖到服务器
        3. 重命名已存在的文章
        4. 删除文章/目录，可以选择是否备份
        5. 以某种方式重新对文章/目录排序：
            可选的排序方式：
                1. 以顺序字母正/倒序
                2. 以上次更新的时间正/倒序
                3. 以创建时间正/倒序
                4. 目录/文件优先
                *. 4可以和1、2、3组合

规范：
    - 底层函数在上
    - 所有函数由小写字母、数字或下划线命名
    - 函数文档应写明参数类型与返回值
    - 每个函数都应有函数概述
    - 每个函数都应被日志打印装饰器装饰
    - 尽可能大的鲁棒性，尽量考虑所有可能发生的情况
    - 单元测试是必要的
    - 为了避免不必要的bug，尽量显式使用深拷贝，
      敏感地对可遍历对象使用赋值或浅拷贝
"""

import os
import sys
import json
import socket
import platform
from copy import deepcopy

SEP_SYMBOL = '\\' if platform.system() == "Windows" else "/"

HOST = "127.0.0.1"
JSON_PORT = 10001
SEND_PORT = 12555

CACHE_PATH = f".{SEP_SYMBOL}.cache.md"

def lslayer__local_list(curlayer):
    keylist = list()
    index = 0
    for key in curlayer:
        if curlayer[key][1] == 0:
            print(f"{index}. File: {key}")
        elif curlayer[key][1] == 1:
            print(f"{index}. Directory: {key}")
        index += 1
        keylist.append(key)
    return keylist

def combine_multi_space__local_str(s) -> str:
    """Merge several consecutive spaces into one"""
    news = s.replace('  ', ' ')
    while news != s:
        s = news
        news = s.replace('  ', ' ')
    return news

def input_article__local_str():
    """Open Vim. Write and then read."""
    os.system(f"vim {CACHE_PATH}")
    with open(CACHE_PATH, "rt") as f:
        raw = f.read()
    return raw

def choose_path_cmd__local_None(curlayer, choose, keylist):
    """Probably mkdir."""
    choose = combine_multi_space__local_str(choose.strip())

    routertmp = CommandRouter(choose.split(' '))
    argdict = deepcopy(routertmp.argdict)

    print(argdict)
    if argdict["__ANONYMOUS"][0] == "mkdir":
        if argdict["__ANONYMOUS"][1] in keylist:
            print(f"Invalid input! The directory already exists.")
        else:
            curlayer[argdict["__ANONYMOUS"][1]] = [argdict["__ANONYMOUS"][2], 1, {}]


"""

"""
def insert_file_to_path_may_mkdir__local_str(json_dict, serious_name, title_name):
    """
    此函数接收参数:
        json_dict: 老的directory.json，需要注意，此函数内部会直接修改json_dict
                   这是一个参数，此函数结束后蕴含了返回的信息
        serious_name, title_name 意义显然

    基于json_dict的结构，此函数会进入一个虚拟目录中，接收用户的命令，根据
    命令的内容来对json_dict进行相应的修改（但这不是这个函数的主要目标），
    此函数主要的目标是让用户选择一个目录或某个具体文件，并返回用户选择的            (返回值)
    目录或具体文件相对于json_dict虚拟目录的路径
    """
    pathstr = ""
    curlayer = json_dict
    while True:
        # keylist 是一个list，其成员为此层curlayer的键值
        # lslayer__local_list函数同时还会输出此层curlayer结构
        keylist = lslayer__local_list(curlayer)

        choose = input("> ")
        try:                            # 输入选择，并转为数字
            choose = int(choose)

            if choose == -1:                # 就是这里
                curlayer[serious_name] = [title_name, 0]
                break
            else:                           # 选择索引
                chosen_key = keylist[choose]
                pathstr += f"{SEP_SYMBOL}{chosen_key}"

                if curlayer[chosen_key][1] == 0:        # 选择的是文件，让pathstr带上文件名之后直接返回
                    break
                elif curlayer[chosen_key][1] == 1:      # 选择的是目录，继续迭代
                    curlayer = curlayer[chosen_key][2]

        except ValueError:              # 若无法成功转为数字，按照指令处理
            choose_path_cmd__local_None(curlayer, choose, keylist)
            continue

    return pathstr


def remove_file_or_path_without_mkdir__local_list(json_dict):
    rm_list = []
    pathstr = ""

    lastlayer = dict()
    last_choice = ""
    curlayer = json_dict
    while True:
        # keylist 是一个list，其成员为此层curlayer的键值
        # lslayer__local_list函数同时还会输出此层curlayer结构
        keylist = lslayer__local_list(curlayer)

        choose = int(input("> "))

        if choose == -1:                # 就是这个目录
            rm_list.append(deepcopy(pathstr))
            del lastlayer[last_choice]
            pathstr = ""
            curlayer = json_dict
        elif choose == -2:              # 够了，滚
            break
        else:                           # 选择索引
            chosen_key = keylist[choose]
            pathstr += f"{SEP_SYMBOL}{chosen_key}"

            if curlayer[chosen_key][1] == 0:        # 选择的是文件，让pathstr带上文件名
                rm_list.append(deepcopy(pathstr))
                del curlayer[chosen_key]
            elif curlayer[chosen_key][1] == 1:      # 选择的是目录，继续迭代
                lastlayer = curlayer
                last_choice = chosen_key
                curlayer = curlayer[chosen_key][2]
    return rm_list

def recv_all__local_bytes(sock, bufsiz=1024) -> bytes:
    """Receive until no more data."""
    data = b''
    while True:
        part = sock.recv(bufsiz)
        data += part
        if len(part) < bufsiz:
            break
    return data

def get_json_from_server__local_dict() -> dict:
    """
    Connect to the specified server,
    receive JSON data,
    parse JSON into a dictionary.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, JSON_PORT))
    raw = recv_all__local_bytes(s).decode("utf-8")
    s.close()
    return json.loads(raw)


def send_to_server__local_None(msg: str):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, SEND_PORT))
    sock.send(msg.encode("utf-8"))
    sock.close()

def add_files_to_server__local_None(new_json, file_raw_dict):
    """
    Send new data to server.
    Args:
        new_json: dict. JSON after adding new articles/directories.
        file_raw_dict: dict. Key is path of article, and value is its raw.
    
    Message format:
        new_json\r\nDATA_RAW_SPLIT\r\nfile_raw_dict

    """
    msgraw = f"S{json.dumps(new_json)}\r\nDATA_RAW_SPLIT\r\n{json.dumps(file_raw_dict)}"
    send_to_server__local_None(msgraw)

class CommandRouter:
    def __init__(self, argv):
        """
        解析参数列表为字典
    
        参数:
            argv: list. 由命令行参数组成的列表（含当前执行的脚本文件名）
        返回值：
            字典：解析得到的字典
            格式：{"__ANONYMOUS": [匿名参数列表], "-x": "value", ...}
        """

        self.argdict = dict()

        arglist = []
        option = ""
        for each in argv:
            if each[0] == '-':
                option = each
                # 在这里append，因为后面hash后相同的key会相撞
                # 不用担心出现[[option1, ""], [option1, value]]的问题
                arglist.append([option, ""])
                continue
    
            if option != "":
                arglist.append([option, each])
                option = ""
            else:
                arglist.append(each)
    

        _argdict = { "__ANONYMOUS": list() }
        for element in arglist:
            if isinstance(element, str):
                _argdict["__ANONYMOUS"].append(element)
            elif isinstance(element, list):
                if len(element) == 2:
                    if isinstance(element[0], str) and isinstance(element[1], str):
                        _argdict[element[0]] = element[1]
                    else:
                        raise TypeError(f"argv_analysis: Element of unexpected " + 
                                        f"type: {element}")
                else:
                    raise IndexError(f"argv_analysis: Unexpected element: {element}")
        self.argdict = deepcopy(_argdict)
        print(self.argdict)



    def route__None(self):
        # python .\\client.py 匿名添加文章
        if len(self.argdict["__ANONYMOUS"]) == 1 and len(self.argdict.keys()) == 1:
            self.add_article_anonymous__None()

        """
        python .\\client.py -a filename [-n title_name] [-s serious_name]
            -a必须有，指定添加哪个文件作为文章      ( -a means add )
            -n设置标题名，-s设置路径名，缺啥补啥
        """
        if "-a" in self.argdict.keys():                  # 添加实名文章
            self.add_article_with_name__None()
        elif "-g" in self.argdict.keys():                  # 从服务器下载文章
            self.download_article__None()
        elif "-x" in self.argdict.keys():               # 删除文件/目录
            self.remove_file_or_path__None()


    def add_article_anonymous__None(self):
        """
            python .\\client.py
                匿名上传文章
        """
        old_data = get_json_from_server__local_dict()
        fileraw = input_article__local_str()
        serious_name = input("serious_name: ")
        title_name = input("title_name: ")

        filepath = insert_file_to_path_may_mkdir__local_str(old_data, serious_name, title_name)
        print(f"filepath: {filepath}")

        new_data = old_data
        add_files_to_server__local_None(new_data, {f"{filepath}{SEP_SYMBOL}{serious_name}": fileraw})



    def add_article_with_name__None(self):
        """
            python .\\client.py -a filename [-n title_name] [-s serious_name]
                -a必须有，指定添加哪个文件作为文章      ( -a means add )
                -n设置标题名，-s设置路径名，缺啥补啥
        """
        # -n -s 缺啥补啥
        if '-n' not in self.argdict.keys():
            self.argdict['-n'] = input("请输入文章的title名: ")
        if '-s' not in self.argdict.keys():
            self.argdict['-s'] = input("请输入文章serious_name: ")

        old_data = get_json_from_server__local_dict()
        print(f"old_data: {type(old_data)}")
        fileraw = ""
        with open(self.argdict['-a'], "rt") as f:
            fileraw = f.read()
        serious_name = self.argdict['-s']
        title_name = self.argdict['-n']

        filepath = insert_file_to_path_may_mkdir__local_str(old_data, serious_name, title_name)
        print(f"filepath: {filepath}")

        new_data = old_data
        add_files_to_server__local_None(new_data, {f"{filepath}{SEP_SYMBOL}{serious_name}": fileraw})


    def download_article__None(self):
        """
            python .\\client.py -g d
                远程下载某篇文章

            报文格式：
                f"G{filepath(with serious_name)}"
        """
        json_data = get_json_from_server__local_dict()
        # TODO...


    def update_with_file__None(self):
        """
            python .\\client.py -u filename
                将filename作为更新内容，更新某篇文章
        """
        pass


    def pull_and_update__None(self):
        """
            python .\\client.py -u p
                先从远程获取先前的文章，再改，改了之后再更新到远程
        """
        pass

    def rename_file__None(self):
        pass

    def rename_article__None(self):
        pass

    def remove_file_or_path__None(self):
        old_data = get_json_from_server__local_dict()
        rm_list = remove_file_or_path_without_mkdir__local_list(old_data)

        data = "$$$".join(rm_list)
        send_to_server__local_None(f"D{old_data}\r\nDATA_RAW_SPLIT\r\n{data}")

    def reorder_by_mode(self):
        pass

if __name__ == '__main__':
    cmd_router = CommandRouter(sys.argv)
    cmd_router.route__None()
