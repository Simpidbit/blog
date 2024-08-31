import json
import copy

FILETYPE_UNDEFINED  = 0
FILETYPE_FILE       = 1
FILETYPE_DIR        = 2


class Filenode:
    def __init__(self,
                 name: str = "__ROOT__",
                 serious_name: str = "__ROOT__",
                 _type: int = 0,
                 children: list = []) -> None:
        self.filename = name
        self.serious_name = serious_name
        self.filetype = _type
        self.children = copy.deepcopy(children)

    def append(self, node) -> None:
        self.children.append(node)

class Filetree:
    def __init__(self, data: dict) -> None:
        self.raw = data
        self.root = Filenode()

        def recur_build(json_data: dict, root: Filenode) -> Filenode:
            root.filetype = FILETYPE_DIR
            for key in json_data:
                tmp = Filenode(json_data[key][0], key)
                if json_data[key][1] == 0:       # 文件
                    tmp.filetype = FILETYPE_FILE
                    root.append(tmp)
                elif json_data[key][1] == 1:     # 目录
                    tmp.filetype = FILETYPE_DIR
                    tmp = recur_build(json_data[key][2], tmp)
                    root.append(tmp)
            return root

        self.root = recur_build(data, self.root)

    def print_tree(self, root = None, tab = "") -> None:
        if root is None:
            root = self.root
        for child in root.children:
            if child.filetype == FILETYPE_FILE:
                print(f"{tab}文件: {child.filename}, serious name: {child.serious_name}")
            elif child.filetype == FILETYPE_DIR:
                print(f"{tab}目录: {child.filename}, serious name: {child.serious_name}")
                self.print_tree(child, tab + "\t")


    def addnode_with_pathlist(self, pathlist, node) -> None:
        cursor = copy.copy(self.root)
        for each_path in pathlist:
            for i in range(0, len(cursor.children)):
                if cursor.children[i].serious_name == each_path:
                    if each_path == pathlist[-1]:
                        cursor.children[i].append(node)
                        return
                    else:
                        cursor = copy.copy(cursor.children[i])
                        break
    
    def parse_to_json(self) -> dict:
        dt = {}

        def parse(node, part):
            for child in node.children:
                if child.filetype == FILETYPE_FILE:
                    part[child.serious_name] = [child.filename, 0]
                elif child.filetype == FILETYPE_DIR:
                    part[child.serious_name] = [child.filename, 1, {}]
                    parse(child, part[child.serious_name][2])
            return part

        return copy.deepcopy(parse(self.root, dt))
