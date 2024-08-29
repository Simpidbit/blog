// 请求navigator JSON数据，并渲染到window.navigatorContainer备用
function render_navigator_from_JSON__interface_navigator() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/data/directory", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            raw = xhr.responseText;
            window.directoryData = JSON.parse(raw);
            window.navigatorContainer = NEW("NAV", { "class": "content-nav" });
            buildDirectoryToCursor(window.navigatorContainer, window.directoryData, "/");
        }
    }
    xhr.send();
}


/*
{
    "hello.md": ["测试", 0],
    "math": ["数学", 1, {
        "bajian": ["拔尖", 1, {
            "note.md": ["笔记", 0]
        }]
    }]
}
*/

// 构建组成navigator的tag，可以是文件，也可以是目录
function create_ele_for_navigator__local_navigator(name, serious_name, unfoldable, parentpath) {
    let tag = NEW("LI", { "data-seriousname": serious_name });
    if (unfoldable == 0) {          // file
        let a = NEW("A", { "href": `javascript:update_markdown_to_main_area__interface_loader(\"${parentpath}${serious_name}\");` });
        a.innerText = "📝 " + name;
        tag.appendChild(a);
    } else if (unfoldable == 1) {   // path
        let details = NEW("DETAILS");
        details.addEventListener("toggle", (event) => {
            if (details.open) {
                console.log("打开", details);
            } else {
                console.log("关闭", details);
            }
        });

        let summary = NEW("SUMMARY");
        let ul = NEW("UL");

        summary.innerText = "📂 " + name;
        details.appendChild(summary);       details.appendChild(ul);
        tag.appendChild(details);
    }
    return tag;
}

// 通过create_ele_for_navigator__local_navigator()创建tag
// 并将这些tag组装起来
// 并写入cursor (此时cursor更像是作为一个容器)
// 注意：cursor_data与cursor并无直接联系
// cursor_data的"cursor"是由于此函数递归调用而得名的
function buildDirectoryToCursor(cursor, cursor_data, path) {
    for (let key in cursor_data) {
        if (cursor_data[key][1] == 0) {         // file
            let tag = create_ele_for_navigator__local_navigator(
                cursor_data[key][0], key, 0, path
            );
            cursor.appendChild(tag);
        } else if (cursor_data[key][1] == 1) {  // path
            let tag = create_ele_for_navigator__local_navigator(
                cursor_data[key][0], key, 1, path
            );
            cursor.appendChild(tag);
            buildDirectoryToCursor(
                tag.firstElementChild.firstElementChild.nextElementSibling,
                cursor_data[key][2],
                path + key + "/"
            );
        }
    }
}

// 前往根目录
// 由 / 按钮的onclick属性调用
// 需要通过async_try_until_ok__interface_wait(gotoMainContent, 0)调用
function gotoMainContent() {
    window.simpidTitleData = null;
    ID("md-content").innerHTML = "";
    let markdown = ID("main-area");
    markdown.innerHTML = "";
    markdown.appendChild(window.navigatorContainer);
    history.replaceState(null, null, "/root");

    markdown.scrollTo(0, 0);
}

// 从cursor元素，沿着patharr展开
// 返回最后一个可以展开的元素(DETAILS)
function unfoldNavigator(cursor, patharr) {
    for (let i = 0; i < patharr.length; i++) {
        let childs = cursor.children;
        for (let j = 0; j < childs.length; j++) {       // 搜索cursor的子节点
            if (childs[j].firstElementChild.tagName == "DETAILS") {         // 子节点包含Details
                if (childs[j].getAttribute("data-seriousname") == patharr[i]) {         // 验证子节点seriousname
                    childs[j].firstElementChild.open = true;
                    if (i == patharr.length - 2) {
                        return childs[j].firstElementChild.firstElementChild;
                    }
                    cursor = childs[j].firstElementChild.firstElementChild.nextElementSibling;      // 更新cursor
                    break;          // 停止搜索，继续下一轮
                }
            }
        }
    }
}

// node是details下的summary
// 将navigator移至对其此details
function moveNavigatorRoot(node, navigator) {
    let details_rect = node.parentElement.getBoundingClientRect();
    let navigator_rect = navigator.getBoundingClientRect();

    navigator.scrollTo(details_rect.x  - navigator_rect.x, details_rect.y - navigator_rect.y);
}


// 前往上层目录
// 由 < 按钮的onclick属性调用
function gotoLastContent() {
    window.simpidTitleData = null;
    ID("md-content").innerHTML = "";

    // 获取地址栏内容并判断上级目录是谁
    let pathname = window.location.pathname;
    paths = pathname.split("/");
    paths.shift();      // ""
    paths.shift();      // "root"

    // 将上级目录写入地址栏
    let newpath = "/root";
    for (let k = 0; k < paths.length - 1; k++) {
        newpath += "/" + paths[k];
    }
    history.replaceState(null, null, "/root");

    // 按照上级目录的位置展开
    let anchorElement = unfoldNavigator(window.navigatorContainer, paths);
    console.log(anchorElement);

    // 将navigator写入主界面（id=markdown）
    let markdown = ID("main-area");
    markdown.innerHTML = "";
    markdown.appendChild(window.navigatorContainer);

    // 移动到上级目录的位置
    if (paths.length <= 1) {
        markdown.scrollTo(0, 0);
    } else {
        moveNavigatorRoot(anchorElement, markdown);
    }
}
