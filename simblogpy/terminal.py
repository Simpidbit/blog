import os

import simblogpy as blog
import simblogpy.filejson
from simblogpy.log import print_func_to_log
from simblogpy.string import SEP_SYMBOL

BEGIN_PATH = f".{SEP_SYMBOL}root"
MAIN_PATH = "."
CACHE_PATH = f"{MAIN_PATH}{SEP_SYMBOL}.blogclientcache"


test_data = \
{
    "program": ["\u9879\u76ee", 1, {
            "blog.md": ["\u6211\u7684\u535a\u5ba2 - \u5f00\u53d1\u6587\u6863", 0]
        }
    ],
    "coding_language": ["\u7f16\u7a0b\u8bed\u8a00", 1, {
            "python3": ["Python3", 1, {
                    "Python3.10_match_case.md": ["Python3.10 \u65b0\u7279\u6027\uff1amatch...case\u8bed\u53e5", 0]
                }
            ]
        }
    ],
    "operating_system": ["\u64cd\u4f5c\u7cfb\u7edf", 1, {
            "linux": ["linux", 1, {
                    "ubuntu": ["Ubuntu", 1, {
                            "Ubuntu_apt_change_source.md": ["Ubuntu apt\u6362\u6e90", 0]
                        }
                    ]
                }
            ]
        }
    ]
}



def choose_path_cmd__None(curlayer, choose, keylist):
    """Probably mkdir."""
    choose = blog.string.combine_multi_space__str(choose.strip())
    argdict = blog.argv.argv_parse_to_dict__dict(choose.split(' '))
    print(argdict)
    if argdict["__ANONYMOUS"][0] == "mkdir":
        if argdict["__ANONYMOUS"][1] in keylist:
            print(f"Invalid input! The directory already exists.")
        else:
            curlayer[argdict["__ANONYMOUS"][1]] = [argdict["__ANONYMOUS"][2], 1, {}]


def choose_path_without_mkdir__str(json_dict):
    """Choose a path, NO mkdir!"""
    pathstr = ""
    curlayer = json_dict
    while True:
        if isinstance(curlayer, dict):
            pass
        else:
            print(f"Unexpected curlayer: {curlayer}")
            print(f"{type(curlayer)}")
        keylist = blog.filejson.lslayer__list(curlayer)

        try:
            choose = input("> ")
            choose = int(choose)
        except ValueError:
            print("Unexpected input!")
            continue

        if choose > len(keylist): raise IndexError("Too big index.")

        if choose == -1:        # TODO
            #print(json_dict)
            break
        else:
            chosen_key = keylist[choose]
            if curlayer[chosen_key][1] == 0:
                pathstr += f"{SEP_SYMBOL}{chosen_key}"
                break
            elif curlayer[chosen_key][1] == 1:
                curlayer = curlayer[chosen_key][2]
        pathstr += f"{SEP_SYMBOL}{chosen_key}"
    print(pathstr)
    return pathstr


"""
Args:
    json_dict: This function will write new keys and values to json_dict

Return:
    str: 
"""
@print_func_to_log
def insert_file_to_path_may_mkdir__str(json_dict, serious_name, title_name):
    """Choose a path, but maybe mkdir."""
    pathstr = ""
    curlayer = json_dict
    while True:
        if isinstance(curlayer, dict):
            pass
        else:
            print(f"Unexpected curlayer: {curlayer}")
            print(f"{type(curlayer)}")
        keylist = blog.filejson.lslayer__list(curlayer)

        try:                            # 输入选择，并转为数字
            choose = input("> ")
            choose = int(choose)

            if choose == -1:                # 就是这里
                curlayer[serious_name] = [title_name, 0]
                print(json_dict)
                break
            elif choose > len(keylist):     # 选择的进入的目录索引过大
                raise IndexError("Too big index.")
            else:                           # 选择的目录索引正常
                chosen_key = keylist[choose]
                if curlayer[chosen_key][1] == 0:        # 选择的是文件，让pathstr带上文件名之后直接返回
                    pathstr += f"{SEP_SYMBOL}{chosen_key}"
                    break
                elif curlayer[chosen_key][1] == 1:      # 选择的是目录，继续迭代
                    curlayer = curlayer[chosen_key][2]
            pathstr += f"{SEP_SYMBOL}{chosen_key}"
        except ValueError:              # 若无法成功转为数字，按照mkdir指令处理
            choose_path_cmd__None(curlayer, choose, keylist)
            continue
    return pathstr


if __name__ == '__main__':
    choose_path_without_mkdir__str(test_data)
