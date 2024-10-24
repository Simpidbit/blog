import copy
import platform

from simblogpy.string import SEP_SYMBOL


test1 = \
{
    "hello.md": ["你好.md", 0],
    "code": ["代码", 1, {
            "python": ["py代码", 1, {
                }
            ],
            "cpp": ["C++代码", 1, {
                    "main.cpp": ["主文件", 0],
                    "test.cpp": ["测试文件", 0]
                }
            ]
        }
    ],
    "program": ["项目", 1, {
            "simskt": ["C++socket", 0]
        }
    ]
}


test2 = \
{
    "hello.md": ["你好.md", 0],
    "code": ["代码", 1, {
            "python": ["py代码", 1, {
                }
            ],
            "cpp": ["C++代码", 1, {
                    "main.cpp": ["主文件", 0],
                    "test.cpp": ["测试文件", 0],
                    "add.cpp": ["附加文件", 0],
                    "src": ["源文件夹", 1, {
                            "vim.c": ["vim源文件", 0],
                            "emacs.c": ["emacs源文件", 0],
                            "gnu": ["gnu项目", 1, {
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ],
    "program": ["项目", 1, {
            "simskt": ["C++socket", 0]
        }
    ]
}

"""
    return点必为空文件夹或文件
"""
def find_newfile_paths(old_data, new_data):
    pass

def build_pathstr_from_list(pathlist):
    pathstr = ""
    for each in pathlist:
        pathstr += f"{SEP_SYMBOL}{each}"
    return pathstr


def scan_file_json_to_path(data, curlist, paths) -> list:
    for key in data:
        if data[key][1] == 1:
            if len(data[key][2].keys()) == 0:
                paths.append([build_pathstr_from_list(curlist + [key]), data[key][1]])
            else:
                scan_file_json_to_path(data[key][2], copy.deepcopy(curlist + [key]), paths)
        else:
            paths.append([build_pathstr_from_list(curlist + [key]), data[key][1]])

def what_type_this_path_is__int(data, filepath) -> int:
    pathlist = filepath.split('/')
    pathlist = pathlist[1:]

    cursor = None
    index = 0
    while True:
        for key in data.keys():
            if key == pathlist[index]:
                if index == len(pathlist) - 1:      # Return
                    return data[key][1]
                cursor = data[key][2]
                index += 1
                break


def get_file_dir__str(filepath) -> str:
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



if __name__ == '__main__':
    paths = []
    scan_file_json_to_path(test2, [], paths)
    [print(i) for i in paths]
