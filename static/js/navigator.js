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
// 从json中解析出符合foldtree的list_data，方便后续foldtree的建立
function parse_list_data_from_JSON__local_navigator(json, level, patharr) {
    let keys = Object.keys(json);
    for (let i = 0; i < keys.length; i++) {
        if (json[keys[i]][1] == 0) {           // 文件
            patharr[level - 1] = keys[i];
            render_foldtree_to_ele_from_globaldata__interface_foldtree(
                [
                    [
                        level,
                        json[keys[i]][0]
                    ]
                ], window.navigator_temp_container, "navigator",
                {
                    "class": "navigator-btn",
                    "onclick": "this.parentElement.firstElementChild.nextElementSibling.click();",
                    "btn-text": "📝",
                    "style": "user-select: none;"
                },
                {
                    "class": "navigator-a",
                    "href": `javascript:update_markdown_to_main_area__interface_loader(\"${get_pathname_from_path_queue__interface_pathque(patharr)}\", false);`
                },
                {
                    "class": "navigator-div"
                }, false, 30);
        } else if (json[keys[i]][1] == 1) {    // 目录
            patharr[level - 1] = keys[i];
            render_foldtree_to_ele_from_globaldata__interface_foldtree(
                [
                    [
                        level,
                        json[keys[i]][0]
                    ]
                ], window.navigator_temp_container, "navigator",
                {
                    "class": "navigator-btn",
                    "btn-text": "📂",
                    "style": "user-select: none;"
                },
                {
                    "class": "navigator-a",
                    "onclick": "this.parentElement.firstElementChild.click();",
                    "style": "user-select: none;"
                },
                {
                    "class": "navigator-div"
                }, false, 30);
            parse_list_data_from_JSON__local_navigator(
                json[keys[i]][2],
                level + 1,
                JSON.parse(JSON.stringify(patharr))     // 必须是深拷贝
            );
        }
    }
}

// 请求navigator JSON数据，并渲染到window.navigator_temp_container备用
function render_navigator_from_JSON__interface_navigator() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/data/directory", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            raw = xhr.responseText;
            window.navigator_temp_container = NEW("div", { "class": "content-nav" });
            let directory_json = JSON.parse(raw);
            window.navigator_json = directory_json;
            render_foldtree_to_ele_from_globaldata__interface_foldtree(
                [],         null,       "navigator",
                null,       null,       null,
                true);
            parse_list_data_from_JSON__local_navigator(directory_json, 1, []);

            // 还要再设置每个label的data-id，因为parse_list_data_from_JSON__local_navigator内部data-id一开始全都是0
            for (let i = 0; i < window.navigator_temp_container.childNodes.length; i++) {
                window.navigator_temp_container.childNodes[i].setAttribute("data-id", i.toString());
            }
        }
    }
    xhr.send();
}


// 前往根目录
// 由 / 按钮的onclick属性调用
// 需要通过async_try_until_ok__interface_wait(goto_main_index__callback_navigator, 0)调用
function goto_main_index__callback_navigator() {
    window.html_title_digest = null;
    ID("md-content").innerHTML = "";
    let markdown = ID("main-area");
    markdown.innerHTML = "";
    markdown.appendChild(window.navigator_temp_container);
    history.replaceState(null, null, "/root");

    markdown.scrollTo(0, 0);
}

// 前往上层目录
// 由 < 按钮的onclick属性调用
function goto_last_content__callback_navigator() {
}
