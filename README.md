# 项目文档



## JS部分

### 执行代码的入口

#### 网页打开时

打开网页时，`main.js`里的`window.onload`回调函数会被调用，`window.onload`调用之外的地方没有自动执行的代码



#### 按钮的回调函数

点击各按钮时，会触发按钮的回调函数

具体如下：

|按钮类型| 按钮说明 | 回调函数 |
|--------| -------- | -------- |
|按钮|返回主目录按钮|`async_try_until_ok__interface_wait(goto_main_index__callback_navigator, 0);`|
|按钮|返回上层目录按钮|`goto_last_content__callback_navigator();`|
|超链接|在目录中点击某个文章，就加载此文章|`update_markdown_to_main_area__interface_loader(...);`|
|超链接| 左侧文章目录栏中的标题，点击时跳转到到文章对应的标题位置|`goto_title_of_mdcontent__callback_mdcontent(this);`|
|按钮|左侧文章目录栏中标题前面的折叠/展开键，点击会折叠或展开|`change_btn_status__callback_mdcontent(this);`<br />`fold_mdcontent_label__callback_mdcontent(this.parentElement);`|



### 各模块及功能说明

#### main.js

主要定义`window.onload`回调函数，刚刚打开时处理页面，同时异步引入较大的MathJax模块



#### mdloader

`markdown.js`及`markdown`目录下的代码负责markdown语法的解析，`loader.js`负责将解析为html的md文件写入main-area并构建左侧的目录



#### mdcontent.js

负责构建页面左侧的目录



#### navigator

负责构建在main-area显示的主目录



#### pathque.js

小模块，负责处理URL中的路径



#### static.js

小模块，对原生JS进行一些封装



#### wait.js

小模块，负责对异步操作进行一些封装



#### external_mermaid

外部引用mermaid，负责渲染mermaid图



#### external_MathJax

外部引用MathJax，负责渲染laTeX公式



### 用到的全局变量(window.xxx)

#### window.html_title_digest

**说明**：扫描html标题结构时，用于保存标题结构，以方便后续左侧目录的构造

**类型**：数组

**结构**：

```javascript
[
    [第几级标题, 标题内容],
    [第几级标题, 标题内容],
    ...
]
    
例如：
[
    [1, "Hello一级标题"],
    [2, "这是第二级标题"]
]
```

**更改此变量的函数**：`scan_html_title__local_mdcontent`、`goto_last_content__callback_navigator`、`goto_main_index__callback_navigator`

**仅读取此变量的函数（不含更改）**：`render_mdcontent_from_globaldata__interface_mdcontent`



#### window.mdcontent_label_state

**说明**：为了实现左侧目录点击时的展开/折叠动作，需要一个变量保存左侧目录中各行的显示状态，即此变量

**类型**：数组

**结构**：

```javascript
[
    [状态, 元素1, 元素2, 元素3, ...],
    [状态, 元素1, 元素2, 元素3, ...],
    ...
]
    
例如：
[
    ["closed", 元素1, 元素2, 元素3],		// 目录中的0号标题折叠
    ["open"]							// 目录中的1号标题展开
]
```

注意：

- "close"后面的元素是被折叠的元素，存在`window.mdcontent_label_state`里是为了方便后续再显示这些元素，"open"后面没有元素
- `window.mdcontent_label_state`的第`i`索引位置保存的即为id为`i`的标题的折叠/展开数据

**更改此变量的函数**：`render_mdcontent_from_globaldata__interface_mdcontent`、`fold_mdcontent_label__callback_mdcontent`



#### window.navigator_temp_container

**说明**：构建navigator时，可能不需要立即在main-area显示navigator，那么构建的navigator就暂时存储为此变量，需要显示时直接从此变量写入main-area即可

**类型**：DOM节点（NAV元素）

**更改此变量的函数**：`render_navigator_from_JSON__interface_navigator`

**仅读取此变量的函数（不含更改）**：`goto_main_index__callback_navigator`、`goto_last_content__callback_navigator`
