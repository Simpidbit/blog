# 导入 json 模块，用于序列化和反序列化 JSON 数据
import json
# 导入 copy 模块，用于创建对象的深拷贝
import copy

# 定义文件类型常数
FILETYPE_UNDEFINED  = 0
FILETYPE_FILE       = 1
FILETYPE_DIR        = 2

# 定义 Filenode 类，代表文件系统中的一个节点
class Filenode:
    def __init__(self,
                 name: str = "__ROOT__",
                 serious_name: str = "__ROOT__",
                 _type: int = 0,
                 children: list = []) -> None:
        """
        初始化 Filenode 对象

        参数：
            name (str): 节点名称，默认为 "__ROOT__"
            serious_name (str): 节点真实名称，默认为 "__ROOT__"
            _type (int): 文件类型（0: 未定义，1: 文件，2: 目录）
            children (list): 子节点列表

        返回：
            None
        """
        # 设置 filename 和 serious_name 属性
        self.filename = name
        self.serious_name = serious_name
        # 设置文件类型
        self.filetype = _type
        # 创建 children 属性的深拷贝，以防止外部修改影响内部状态
        self.children = copy.deepcopy(children)

    def append(self, node) -> None:
        """
        在当前节点下添加一个子节点

        参数：
            node：要添加的子节点

        返回：
            None
        """
        # 使用 append() 方法将子节点添加到 children 列表
        self.children.append(node)

# 定义 Filetree 类，代表文件系统中的目录树
class Filetree:
    def __init__(self, data: dict) -> None:
        """
        初始化 Filetree 对象

        参数：
            data (dict): 包含文件名和文件类型信息的字典

        返回：
            None
        """
        # 保存原始数据
        self.raw = data
        # 创建 Filenode 对象作为树的根节点
        self.root = Filenode()
        # 递归构建目录树
        self.root = self.recur_build(data, self.root)

    def recur_build(self, json_data: dict, root: Filenode) -> Filenode:
        """
        递归地构建目录树

        参数：
            json_data (dict): 包含文件名和文件类型信息的字典
            root (Filenode): 当前递归的根节点

        返回：
            Filenode: 构建完成的目录树根节点
        """
        # 将当前节点设置为目录类型
        root.filetype = FILETYPE_DIR
        for key in json_data:
            # 创建临时 Filenode 对象
            tmp = Filenode(json_data[key][0], key)
            # 判断是否为文件
            if json_data[key][1] == 0:
                # 设置文件类型
                tmp.filetype = FILETYPE_FILE
                # 将文件节点添加到当前节点的子节点列表
                root.append(tmp)
            elif json_data[key][1] == 1:
                # 设置目录类型
                tmp.filetype = FILETYPE_DIR
                # 递归构建子目录并更新临时节点
                tmp = self.recur_build(json_data[key][2], tmp)
                # 将子目录节点添加到当前节点的子节点列表
                root.append(tmp)
        return root

    def print_tree(self, root = None, tab = "") -> None:
        """
        打印文件目录树

        参数：
            root (Filenode): 要打印的根节点，默认为 None，即从整个目录树的根节点开始打印
            tab (str): 用于缩进显示的制表符

        返回：
            None
        """
        if root is None:
            # 如果未提供根节点，则使用目录树的根节点
            root = self.root
        for child in root.children:
            if child.filetype == FILETYPE_FILE:
                # 打印文件信息
                print(f"{tab}文件: {child.filename}, serious name: {child.serious_name}")
            elif child.filetype == FILETYPE_DIR:
                # 打印目录信息
                print(f"{tab}目录: {child.filename}, serious name: {child.serious_name}")
                # 递归打印子目录
                self.print_tree(child, tab + "\t")

    def addnode_with_pathlist(self, pathlist, node) -> None:
        """
        根据文件路径列表添加节点

        参数：
            pathlist (list): 文件路径列表，每个元素代表目录路径的一部分
            node (Filenode): 要添加的节点

        返回：
            None
        """
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
        """
        将文件目录树转换为 JSON 格式的字典

        返回：
            dict: 包含文件目录树信息的字典
        """
        dt = {}
        # 内部函数，用于递归地将节点转换为 JSON 字典
        def parse(node, part):
            for child in node.children:
                if child.filetype == FILETYPE_FILE:
                    part[child.serious_name] = [child.filename, 0]
                elif child.filetype == FILETYPE_DIR:
                    part[child.serious_name] = [child.filename, 1, {}]
                    parse(child, part[child.serious_name][2])
            return part
        # 调用递归函数，并使用 deepcopy 确保返回字典的独立性
        return copy.deepcopy(parse(self.root, dt))

