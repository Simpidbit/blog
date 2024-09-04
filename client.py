"""
Excogitation:
    There are mainly the following functions:
        - Add new articles.
        - Update existing articles.
            One way:
                Get an existing article from server, and modify it in terminal,
                then submit modified article to server.
            Another way:
                Submit local file, and overwrite the corresponding article on 
                the server.
        3. Rename existing articles.
        4. Delete articles/directory, backup optionally.
        5. Reorder the articles.
            Optional sorting modes:
                1. Sort in alphabetical order by letters.
                2. Sort in reverse alphabetical order by letters.
                3. Sort in the order of the last update time.
                4. Sort in the reverse order of the last update time.
                5. Sort by creation time.
                6. Sort by creation time in descending order.
                7. Directories comes first, and files come last.
                8. Files come first, and directories come last.
                These modes can be combined with each other.

Specification:
    - Functions that are closer to the bottom layer are placed earlier.
    - All functions are named in lowercase letters and underline(_).
    - The function documentation should clearly state the types of parameters
      and the return value.
    - A function which is called by just one function should be written as
      a nested function.
    - The function overview should be written in the documentation of each
      function.
    - Every function should be decorated by a decorator, which will print
      messages to log file at the beginning and the end of the function.
    - As large robustness as possible. All probabilities should be considered.
    - A decorator for unit testing is required. Every function should undergo
      unit testing.
    - To avoid unnecessary bugs, deep copy should be used as much as possible.
      Be cautious when using assignment and shallow copy.
"""

import os
import sys
import json
import socket
import platform
from copy import deepcopy

import simblogpy as blog
import simblogpy.argv
import simblogpy.correspond
import simblogpy.log
import simblogpy.string
from simblogpy.string import SEP_SYMBOL
import simblogpy.filejson
import simblogpy.correspond
import simblogpy.terminal


"""
    python .\\client.py
        Anonymous article addition.
"""
def add_article_anonymous__None():
    old_data = blog.correspond.get_json_from_server__dict()
    print(f"old_data: {type(old_data)}")
    fileraw = blog.terminal.input_article__str()
    serious_name = input("serious_name: ")
    title_name = input("title_name: ")

    filepath = blog.terminal.choose_path_may_mkdir__str(old_data, serious_name, title_name)
    print(f"filepath: {filepath}")

    new_data = old_data
    blog.correspond.add_files_to_server__None(new_data, {f"{filepath}{SEP_SYMBOL}{serious_name}": fileraw})


"""
    python .\\client.py -a filename [-n titlename] [-s serious_name]
        Add article with titlename. If -s is given, then specify the serious_name of the article.
                                    If not, then require the user to input a serious_name.
"""
def add_article_with_name__None(argdict: dict):
    if '-n' not in argdict.keys():
        argdict['-n'] = input("请输入文章的title名: ")
    if '-s' not in argdict.keys():
        argdict['-s'] = input("请输入文章serious_name: ")
    old_data = blog.correspond.get_json_from_server__dict()
    print(f"old_data: {type(old_data)}")
    fileraw = ""
    with open(argdict['-a'], "rt") as f:
        fileraw = f.read()
    serious_name = argdict['-s']
    title_name = argdict['-n']

    filepath = blog.terminal.choose_path_may_mkdir__str(old_data, serious_name, title_name)
    print(f"filepath: {filepath}")

    new_data = old_data
    blog.correspond.add_files_to_server__None(new_data, {f"{filepath}{SEP_SYMBOL}{serious_name}": fileraw})


"""
    python .\\client.py -g d
        远程下载某篇文章
"""
def download_article__None():
    pass


"""
    python .\\client.py -u filename
        将filename作为更新内容，更新某篇文章
"""
def update_with_file__None():
    pass


"""
    python .\\client.py -u p
        先从远程获取先前的文章，再改，改了之后再更新到远程
"""
def pull_and_update__None():
    pass

def rename_file__None():
    pass

def rename_article__None():
    pass

def remove_file_or_path__None():
    pass

def reorder_by_mode():
    pass

"""
命令:
    python .\\client.py
        Anonymous article addition.
    python .\\client.py -a filename [-n name] [-s serious_name]
        添加名为name的文章, 若有-s选项，则指定文章serious_name，若没有，则默认filename为文章的serious_name


    python .\\client.py -g
        远程下载某篇文章


    python .\\client.py -u filename
        将filename作为更新内容，更新某篇文章
    python .\\client.py -u
        先从远程获取先前的文章，再改，改了之后再更新到远程


    python .\\client.py -r
        给某篇文章改名


    python .\\client.py rm
        删除某篇文章/某个路径


    python .\\client.py -o ordermethod
        以某种标准对文章/目录重新排序
"""
def route_based_argdict__None(argdict):
    if len(argdict["__ANONYMOUS"]) == 1:        # Anonymous article addition
        add_article_anonymous__None()
    if "-a" in argdict.keys():                  # Add article with name
        add_article_with_name__None()


if __name__ == '__main__':
    argdict = blog.argv.argv_parse_to_dict__dict(sys.argv)
    route_based_argdict__None(argdict)
