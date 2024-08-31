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
    operating_system = platform.system()
    serious_name = str()
    if operating_system == "Windows":
        serious_name = filepath.split('\\')[-1]
    elif operating_system == "Linux" or operating_system == "Darwin":
        serious_name = filepath.split('/')[-1]
    return serious_name


def update_passage(filepath):
    pass

def send_passage(filepath, filename = None):
    if filename is None:
        filename = input("文章名: ")

    file_serious_name = get_serious_name_from_path(filepath)

    tree = Filetree(json.loads(network.get_json_from_server()))

    root_cursor = copy.copy(tree.root)
    pathlist = []
    while True:
        # 列出文件/目录
        index = 0
        print("即将列出..")
        for child in root_cursor.children:
            if child.filetype == FILETYPE_FILE:
                print(f"{index}. 文件: {child.serious_name} 名称: {child.filename}")
            elif child.filetype == FILETYPE_DIR:
                print(f"{index}. 目录: {child.serious_name} 名称: {child.filename}")
            index += 1

        while True:
            try:
                option = input("请选择:")
                option = int(option)
            except ValueError:
                pass

            if isinstance(option, int):     # 数字选项
                if option == -1:            # 就在这里
                    print(pathlist)
                    tree.addnode_with_pathlist(pathlist, Filenode(filename, file_serious_name, FILETYPE_FILE))
                    tree.print_tree()
                    network.send_add(tree.parse_to_json(), filepath)
                    exit()
                else:
                    if root_cursor.children[option].filetype == FILETYPE_DIR:
                        pathlist.append(root_cursor.children[option].serious_name)
                        root_cursor = copy.copy(root_cursor.children[option])
                        print("即将break...")
                        break
                    elif root_cursor.children[option].filetype == FILETYPE_FILE:       # 是更新
                        yes_or_no = input("确定吗？(y/n): ")
                        if yes_or_no == 'n':
                            pass
                        elif yes_or_no == 'y':
                            pathlist.append(root_cursor.children[option].serious_name)
                            network.update_add(pathlist, filepath)
                            exit()
            elif isinstance(option, str):   # 字符串选项
                # 合并多个连续空格
                option = combine_multi_space(option)

                arg_pieces = option.split(' ')
                cmd = arg_pieces[0]

                if cmd == 'mkdir':
                    new_dir_serious_name = arg_pieces[1]
                    new_dir_funny_name = arg_pieces[2]
                    root_cursor.append(Filenode(new_dir_funny_name, new_dir_serious_name, FILETYPE_DIR))
                    break


    

def delete_passage():
    server_json = get_json_from_server()
    tree = Filetree(server_json)
    for each in tree.root.children:
        pass


FUNC_TEXT = """
功能:
    1. 添加/更新文章
    2. 从服务器删除文章
"""
def main():
    if os.system("clear") == 1:
        os.system("CLS")
    print(FUNC_TEXT)
    if len(sys.argv) == 1:
        delete_passage()
    elif len(sys.argv) == 2:
        send_passage(sys.argv[1])
    elif len(sys.argv) == 3:
        send_passage(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
