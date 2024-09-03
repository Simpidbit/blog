import os

import simblogpy as blog
from simblogpy.log import print_func_to_log
from simblogpy.string import SEP_SYMBOL

BEGIN_PATH = f".{SEP_SYMBOL}root"
MAIN_PATH = "."
CACHE_PATH = f"{MAIN_PATH}{SEP_SYMBOL}.blogclientcache"


@print_func_to_log
def input_article__str():
    """Open Vim. Write and then read."""
    os.system(f"vim {CACHE_PATH}")
    with open(CACHE_PATH, "rt") as f:
        raw = f.read()
    return raw

@print_func_to_log
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


@print_func_to_log
def choose_path_may_mkdir__str(json_dict, serious_name, title_name):
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

        try:
            choose = input("> ")
            choose = int(choose)
        except ValueError:
            choose_path_cmd__None(curlayer, choose, keylist)
            continue

        if choose > len(keylist): raise IndexError("Too big index.")

        if choose == -1:
            curlayer[serious_name] = [title_name, 0]
            print(json_dict)
            break
        else:
            chosen_key = keylist[choose]
            if curlayer[chosen_key][1] == 0:
                pathstr += f"{SEP_SYMBOL}{chosen_key}"
                break
            elif curlayer[chosen_key][1] == 1:
                curlayer = curlayer[chosen_key][2]
        pathstr += f"{SEP_SYMBOL}{chosen_key}"
    return pathstr
