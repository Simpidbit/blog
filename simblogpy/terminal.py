import os

import simblogpy as blog
import simblogpy.filejson
from simblogpy.log import print_func_to_log
from simblogpy.string import SEP_SYMBOL

BEGIN_PATH = f".{SEP_SYMBOL}root"
MAIN_PATH = "."
CACHE_PATH = f"{MAIN_PATH}{SEP_SYMBOL}.blogclientcache"


test_data = {"program": ["\u9879\u76ee", 1, {"blog.md": ["\u6211\u7684\u535a\u5ba2 - \u5f00\u53d1\u6587\u6863", 0]}],"coding_language": ["\u7f16\u7a0b\u8bed\u8a00", 1, {"python3": ["Python3", 1, {"Python3.10_match_case.md": ["Python3.10 \u65b0\u7279\u6027\uff1amatch...case\u8bed\u53e5", 0]}]}],"operating_system": ["\u64cd\u4f5c\u7cfb\u7edf", 1, {"linux": ["linux", 1, {"ubuntu": ["Ubuntu", 1, {"Ubuntu_apt_change_source.md": ["Ubuntu apt\u6362\u6e90", 0]}]}]}]}



if __name__ == '__main__':
    choose_path_without_mkdir__str(test_data)
