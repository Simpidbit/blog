import os
import sys
import platform
import copy

import network

from fileman import Filenode, Filetree
from fileman import FILETYPE_FILE, FILETYPE_UNDEFINED, FILETYPE_DIR
from stringwrap import combine_multi_space
import json


def get_serious_name_from_path(filepath) -> str:
    """
    根据文件路径获取文件名

    在Windows系统中，使用反斜杠（\\）作为路径分隔符。

    在Linux和Darwin（Mac OS）系统中，使用正斜杠（/）作为路径分隔符。

    参数:
    filepath (str): 文件的完整路径

    返回:
    str: 从filepath中提取的文件名
    """
    # 获取当前运行的操作系统
    operating_system = platform.system()
    # 初始化文件名
    serious_name = str()
    if operating_system == "Windows":
        # 如果是Windows系统，使用反斜杠分割路径，并取最后一部分作为文件名
        serious_name = filepath.split('\\')[-1]
    elif operating_system == "Linux" or operating_system == "Darwin":
        # 如果是Linux或Mac OS系统，使用正斜杠分割路径，并取最后一部分作为文件名
        serious_name = filepath.split('/')[-1]
    return serious_name


def update_passage(filepath):
    pass

def send_passage(filepath, filename=None):
    """
    发送文章到指定路径。如果未指定文件名，则要求用户输入文件名。

    参数：
        filepath (str): 文件路径。
        filename (str): 文件名。如果未指定，则通过 input 函数要求用户输入。

    返回：
        None

    """
    if filename is None:
        # 如果没有指定文件名，通过input函数要求用户输入
        filename = input("文章名: ")

    # 获取文件名
    file_serious_name = get_serious_name_from_path(filepath)

    # 从服务器获取JSON数据并构建Filetree对象
    tree = Filetree(json.loads(network.get_json_from_server()))

    # 复制Filetree对象的根节点，用于遍历目录结构
    root_cursor = copy.copy(tree.root)
    # 初始化路径列表
    pathlist = []
    while True:
        # 列出文件/目录
        index = 0
        # 打印即将列出的文件/目录
        print("即将列出..")
        for child in root_cursor.children:
            if child.filetype == FILETYPE_FILE:
                # 如果是文件，打印文件名
                print(f"{index}. 文件: {child.serious_name} 名称: {child.filename}")
            elif child.filetype == FILETYPE_DIR:
                # 如果是目录，打印目录名
                print(f"{index}. 目录: {child.serious_name} 名称: {child.filename}")
            index += 1

        while True:
            try:
                # 获取用户输入的选项
                option = input("请选择:")
                # 将用户输入的选项转换为整数类型
                option = int(option)  
            except ValueError:
                pass

            if isinstance(option, int):  # 数字选项
                if option == -1:  # 表示用户选择了“在这里”
                    # 打印当前的路径列表
                    print(pathlist)
                    # 将用户选择的路径添加到Filetree对象中
                    tree.addnode_with_pathlist(pathlist, Filenode(filename, file_serious_name, FILETYPE_FILE))
                    # 将Filetree对象转换为JSON格式的字符串并发送到服务器
                    network.send_add(tree.parse_to_json(), filepath)
                    # 退出程序
                    exit()
                else:
                    # 如果用户选择的是目录
                    if root_cursor.children[option].filetype == FILETYPE_DIR:
                        # 将目录名添加到路径列表中
                        pathlist.append(root_cursor.children[option].serious_name)
                        # 复制被选择目录的节点，用于继续遍历
                        root_cursor = copy.copy(root_cursor.children[option])
                        # 打印即将break，表示程序将继续执行下一个循环
                        print("即将break...")
                        break
                    elif root_cursor.children[option].filetype == FILETYPE_FILE:  # 表示是更新操作
                        # 询问用户是否确定更新文件
                        yes_or_no = input("确定吗？(y/n): ")
                        if yes_or_no == 'n':
                            pass
                        elif yes_or_no == 'y':
                            # 将文件名添加到路径列表中
                            pathlist.append(root_cursor.children[option].serious_name)
                            # 发起更新请求到服务器
                            network.update_add(pathlist, filepath)
                            # 退出程序
                            exit()
            elif isinstance(option, str):  # 字符串选项
                # 合并用户输入字符串中的多个连续空格
                option = combine_multi_space(option)

                # 将用户输入的字符串分割成命令和参数
                arg_pieces = option.split(' ')
                # 获取命令
                cmd = arg_pieces[0]

                if cmd == 'mkdir':
                    # 获取目录的实际名称
                    new_dir_serious_name = arg_pieces[1]
                    # 获取目录的显示名称
                    new_dir_funny_name = arg_pieces[2]
                    # 在当前目录下创建新的目录节点
                    root_cursor.append(Filenode(new_dir_funny_name, new_dir_serious_name, FILETYPE_DIR))
                    break
 

def delete_passage():
    # 从服务器获取JSON数据
    server_json = get_json_from_server()
    # 构建Filetree对象
    tree = Filetree(server_json)
    # 遍历Filetree对象的根节点的子节点
    for each in tree.root.children:
        pass
    
def main():
    """
    主函数，根据传入的参数执行不同的操作

    如果没有传入参数，调用 delete_passage()
    如果传入一个参数，调用 send_passage(sys.argv[1])
    如果传入两个参数，调用 send_passage(sys.argv[1], sys.argv[2])
    """
    if len(sys.argv) == 1:
        # 如果没有传入参数，调用delete_passage函数
        delete_passage()
    elif len(sys.argv) == 2:
        # 如果传入一个参数，将其作为文件路径，调用send_passage函数
        send_passage(sys.argv[1])
    elif len(sys.argv) == 3:
        # 如果传入两个参数，将第一个作为文件路径，第二个作为文件名，调用send_passage函数
        send_passage(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    # 如果当前脚本作为主程序运行，执行main函数
    main()

