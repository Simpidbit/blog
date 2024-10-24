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

**接口**：

- > `catch_plain_text_from_element__local_loader(element)`

  输入：`element`参数，即捕捉哪个元素下的子纯文本节点

  输出：将捕捉到的纯文本套上标签后写回element

- > `update_markdown_to_main_area__interface_loader(path, firstTime = false)`

  输入：

  ​	`path`参数：请求的文章路径（不含root）;

  ​	`firstTime`参数：是否是第一次打开网页;

  ​	`CLASS("mdtag-mermaid")`：将这些节点渲染为mermaid图;

  输出：

  ​	要写入到main-area的文章路径写入地址栏;

  ​	请求的文章写入`ID("main-area")`；

  ​	`CLASS("mdtag-mermaid")`渲染为mermaid；

  ​	



#### mdcontent.js

负责构建页面左侧的目录

**接口**：

- > `render_mdcontent_from_globaldata__interface_mdcontent()`

  输入：

  ​	`window.html_title_digest`数据，用于构建目录

  ​	`ID("md-content")` 被写入的元素

  输出：

   	写入`window.mdcontent_label_state`当前各目录label的状态

  ​	 写入`ID("md-content")`显示目录

  

**回调**：

- > `goto_title_of_mdcontent__callback_mdcontent(a_tag)`

  输入：

  ​	`a_tag`参数：调用这个函数的超链接元素

  ​	`CLASS("mdtag-h")`：从这里面找到是要跳转到哪个标题

  输出：

  ​	跳转到指定标题

  ​	
- > `change_btn_status__callback_mdcontent(btn)`

  输入：

  ​	`btn`参数：调用这个函数的按钮元素，获取此元素父节点的`data-status`属性作为输入
  
  输出：
  
  ​	更改元素父节点的`data-status`属性
  
  ​	
  
- > `fold_mdcontent_label__callback_mdcontent(md_content_label)`
  
  输入：
  
  ​	`md_content_label`参数：调用此函数的元素
  
  ​	已经构造好的`window.mdcontent_label_state`：从这里分析需要展开/折叠哪些元素
  
  输出：
  
  ​	更新`window.mdcontent_label_state`的状态
  
  ​	展开或折叠左侧标题目录栏的某部分
  
  



#### navigator

负责构建在main-area显示的主目录

**接口：**

- > `render_navigator_from_JSON__interface_navigator()`

  输入：

  ​	从服务器请求文件目录的JSON

  输出：

  ​	将构造好的navigator写入`window.navigator_temp_container`

**回调：**

- > `goto_main_index__callback_navigator()`

  输入：

  ​	`window.navigator_temp_container`中构造好的节点

  输出：

  ​	清空`ID("md-content")`

  ​	将构造好的节点写入`ID("main-area")`，同时将地址栏路径改为`/root`

- > `goto_last_content__callback_navigator()`

  输入：

  ​	地址栏中的路径，用来确定文章上级目录是哪个

  ​	`window.navigator_temp_container`中构造好的节点

  输出：

  ​	将构造好的节点写入`ID("main-area")`

  ​	自动让navigator跳转到上级目录的位置

  ​	将`/root`写入地址栏路径



`测试
换行`


#### foldtree.js

是一个抽象的节点树

**接口**：

- > ` render_foldtree_to_ele_from_globaldata__interface_foldtree(
  >  list_data,    ele,       key,
  >  btn_attributes,    a_attributes,   div_attributes，` 
  >
  > `whether_clear)`

​	输入：

​		`list_data`：以列表的形式顺序列出所有label，格式：[ [逻辑层级, 内容], [逻辑层级, 内容], ... ]

​		`ele`：这棵树写到哪个元素上

​		`key`：树的名字，关系到树的临时数据存放

​		`btn_attributes`：折叠按钮的属性，键值对的value为函数时，键对应的值为函数的返回值，函数传入参数(list_data, 此时list_data的索引位置)，下同

​		`a_attributes`：折叠按钮后面链接（内容）的属性

​		`div_attributes`：一对超链接和按钮组成的label的属性

​		`whether_clear`：布尔值，是否清空`window.foldtree_isfold_data[key]`的数据

  	输出：

​		节点树写入`ele`元素

​		将这棵树的折叠数据写入`window.foldtree_isfold_data[key]`

  ​	

  



#### pathque.js

小模块，负责处理URL中的路径



#### static.js

小模块，对原生JS进行一些封装



#### wait.js

小模块，负责对异步操作进行一些封装

**接口**：

- > `async_try_until_ok__interface_wait(func, ms, args = null)`

  输入> 你哈o

  ​	`func`函数，即要异步反复尝试执行的函数本体

  ​	`ms`参数，两次尝试之间等待的毫秒数

  ​	`args`参数，传给`func`的参数，如果为`null`则不给`func`传参

  输出：

  ​	`func`执行成功返回的返回值



#### external_mermaid

外部引用mermaid，负责渲染mermaid图



#### external_MathJax

外部引用MathJax，负责渲染laTeX公式



### 用到的全局变量(window.xxx)

#### window.foldtree_isfold_data

**说明**：为了实现折叠树点击时的展开/折叠动作，需要一个变量保存各折叠树各行的显示状态，即此变量

**类型**：数组

**结构**：

```javascript
{
    树名: [
        树附着的元素, 
        [
        	[状态, 元素1, 元素2, 元素3, ...],
    		[状态, 元素1, 元素2, 元素3, ...],
    		...
    	]
    ]
}
    
状态例如：
[
    ["closed", 元素1, 元素2, 元素3],		// 目录中的0号标题折叠
    ["open"]							// 目录中的1号标题展开
]
```

注意：

- "close"后面的元素是被折叠的元素，存在`window.foldtree_isfold_data`里是为了方便后续再显示这些元素，"open"后面没有元素
- `window.foldtree_isfold_data`的第`i`索引位置保存的即为id为`i`的标题的折叠/展开数据

**更改此变量的函数**：`render_foldtree_to_ele_from_globaldata__interface_foldtree`、`fold_foldtree_label__callback_mdcontent`



#### window.navigator_temp_container

**说明**：构建navigator时，可能不需要立即在main-area显示navigator，那么构建的navigator就暂时存储为此变量，需要显示时直接从此变量写入main-area即可

**类型**：DOM节点（NAV元素）

**更改此变量的函数**：`render_navigator_from_JSON__interface_navigator`

**仅读取此变量的函数（不含更改）**：`goto_main_index__callback_navigator`、`goto_last_content__callback_navigator`
