# 项目文档



## JS部分

### 代码入口

#### 第一处

打开网站时，`main.js`里的`window.onload`回调函数会被调用，`window.onload`调用之外的地方没有自动执行的代码



#### 第二处

点击各按钮时，会触发按钮的回调函数

具体如下：

|按钮类型| 按钮说明 | 回调函数 |
|--------| -------- | -------- |
|按钮|返回主目录按钮|`async_try_until_ok__interface_wait(goto_main_index__callback_navigator, 0);`|
|按钮|返回上层目录按钮|`goto_last_content__callback_navigator();`|
|超链接|在目录中点击某个文章，就加载此文章|`update_markdown_to_main_area__interface_loader(...);|
|超链接| 左侧文章目录栏中的标题，点击时跳转到到文章对应的标题位置|`goto_title_of_mdcontent__callback_mdcontent(this);`|
|按钮|左侧文章目录栏中标题前面的折叠/展开键，点击会折叠或展开|`change_btn_status__callback_mdcontent(this);`<br />`fold_mdcontent_label__callback_mdcontent(this.parentElement);`|

