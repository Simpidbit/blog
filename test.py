import articles

from fileman import Filenode, Filetree
from fileman import FILETYPE_FILE, FILETYPE_UNDEFINED, FILETYPE_DIR
from serverman import find_newfile_path, test_data, test_data2
from serverman import send_handler

if __name__ == '__main__':
    send_handler(test_data2, "#TEST")
