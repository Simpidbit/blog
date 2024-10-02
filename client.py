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

import simblogpy as blog
import simblogpy.correspond
import simblogpy.log
import simblogpy.string
from simblogpy.string import SEP_SYMBOL
import simblogpy.filejson
import simblogpy.correspond
import simblogpy.terminal


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



    def route__None(self):
        # python .\\client.py 匿名添加文章
        if len(self.argdict["__ANONYMOUS"]) == 1:
            self.add_article_anonymous__None()

        """
        python .\\client.py -a filename [-n title_name] [-s serious_name]
            -a必须有，指定添加哪个文件作为文章      ( -a means add )
            -n设置标题名，-s设置路径名，缺啥补啥
        """
        if "-a" in self.argdict.keys():                  # 添加实名文章
            self.add_article_with_name__None()
        if "-g" in self.argdict.keys():                  # 从服务器下载文章
            self.download_article__None()


    def add_article_anonymous__None(self):
        """
            python .\\client.py
                匿名上传文章
        """
        old_data = blog.correspond.get_json_from_server__dict()
        print(f"old_data: {type(old_data)}")
        fileraw = blog.terminal.input_article__str()
        serious_name = input("serious_name: ")
        title_name = input("title_name: ")

        filepath = blog.terminal.insert_file_to_path_may_mkdir__str(old_data, serious_name, title_name)
        print(f"filepath: {filepath}")

        new_data = old_data
        blog.correspond.add_files_to_server__None(new_data, {f"{filepath}{SEP_SYMBOL}{serious_name}": fileraw})



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

        old_data = blog.correspond.get_json_from_server__dict()
        print(f"old_data: {type(old_data)}")
        fileraw = ""
        with open(self.argdict['-a'], "rt") as f:
            fileraw = f.read()
        serious_name = self.argdict['-s']
        title_name = self.argdict['-n']

        filepath = blog.terminal.insert_file_to_path_may_mkdir__str(old_data, serious_name, title_name)
        print(f"filepath: {filepath}")

        new_data = old_data
        blog.correspond.add_files_to_server__None(new_data, {f"{filepath}{SEP_SYMBOL}{serious_name}": fileraw})


    def download_article__None(self):
        """
            python .\\client.py -g d
                远程下载某篇文章

            报文格式：
                f"G{filepath(with serious_name)}"
        """
        json_data = blog.correspond.get_json_from_server__dict()
        filepath = blog.terminal.choose_path_without_mkdir__str(json_data)


    """
        python .\\client.py -u filename
            将filename作为更新内容，更新某篇文章
    """
    def update_with_file__None(self):
        pass


    """
        python .\\client.py -u p
            先从远程获取先前的文章，再改，改了之后再更新到远程
    """
    def pull_and_update__None(self):
        pass

    def rename_file__None(self):
        pass

    def rename_article__None(self):
        pass

    def remove_file_or_path__None(self):
        pass

    def reorder_by_mode(self):
        pass

if __name__ == '__main__':
    cmd_router = CommandRouter(sys.argv)
    cmd_router.route()
