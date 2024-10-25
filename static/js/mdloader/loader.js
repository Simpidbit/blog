// 等待mathJax加载完成
// 初次加载mathJax，每200ms一次尝试加载
// 抓捕element元素下的游离的文本节点
// 将其设为div, class="md-plain-text"
// 
// local函数，只在此文件内被调用
// 调用此函数的函数：update_markdown_to_main_area__interface_loader
function catch_plain_text_from_element__local_loader(element) {
    let mainchilds = element.childNodes;
    for (let i = 0; i < mainchilds.length; i++) {
        if (mainchilds[i].nodeName == "#text") {
            if (mainchilds[i].nodeValue.trim().length == 0) continue;
            let div = NEW("DIV", { "class": "md-plain-text" });
            if (mainchilds[i - 1].tagName == "BR" && mainchilds[i - 2] == "BR") {
                div.innerHTML = "&nbsp;".repeat(7) + mainchilds[i].nodeValue;
            } else {
                div.innerHTML = mainchilds[i].nodeValue;
            }
            element.replaceChild(div, mainchilds[i]);
        }
    }
}

// 请求指定path的markdown，将其刷入网页中并重新渲染
// 此函数还会改变地址栏的地址，但并不会重新加载整个页面
// 从服务器请求markdown数据 --> 渲染markdown数据 --> 写入main-area
//                   --> 加载MathJax --> 构建md-content --> 抓捕游离的普通文本
// Arguments: 
//      path        -       字符串，请求的markdown路径(不含/root)
//      firstTime   -       布尔值，是否是第一次访问，决定尝试加载MathJax的频率
// 无返回值
function update_markdown_to_main_area__interface_loader(path, firstTime = false) {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "/markdown" + path, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            raw = xhr.responseText;
            let markdown = ID("main-area");
            markdown.innerHTML = "";
            markdown.innerHTML = parse_markdown_to_html__local_markdown(raw);
            // 备案号悬挂
            markdown.innerHTML += "<br /><br /><br /><hr /><a href=\"https://beian.miit.gov.cn/\" target=\"_blank\">皖ICP备2024060108号-1</a>&nbsp;&nbsp;<a href=\"http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=51012202001933\" target=\"_blank\">川公网安备51012202001933号</a><br /><br />";
            render_all_elements_to_mermaid__interface_mermaid(CLASS("mdtag-mermaid"));
            history.replaceState(null, null, "/root" + path);
            if (firstTime)  async_try_until_ok__interface_wait(MathJax.typeset, 200);
            else            async_try_until_ok__interface_wait(MathJax.typeset, 0);
            render_mdcontent_from_globaldata__interface_mdcontent();
            catch_plain_text_from_element__local_loader(ID("main-area"));
        }
    }
    xhr.send();
}
