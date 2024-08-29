// 扫描页面中的.mdtag-h
// 并写入window.html_title_digest
// window.html_title_digest: 
//  [
//      [第几级标题, 标题内容],
//      [第几级标题, 标题内容],
//      [第几级标题, 标题内容],
//      ....
//  ]
function scan_html_title__local_mdcontent() {
    window.html_title_digest = [];
    let titles = CLASS("mdtag-h");
    for (let k = 0; k < titles.length; k++) {
        window.html_title_digest.push([
            Number(titles[k].tagName.substr(1)),
            titles[k].innerHTML
        ]);
    }
}


// 依据window.html_title_digest中的数据
// 构建md-content组件并写入左侧边栏
function render_mdcontent_from_globaldata__interface_mdcontent() {
    scan_html_title__local_mdcontent();

    window.mdcontent_label_state = [];
    let md_content = ID("md-content");
    let title_data = window.html_title_digest;
    for (let i = 0; i < title_data.length; i++) {

        let button = NEW("BUTTON", {
            "class": "md-content-button",
            "onclick": "change_btn_status__callback_mdcontent(this);fold_mdcontent_label__callback_mdcontent(this.parentElement);",
            "data-status": "unfolded"
        });
        button.innerHTML = "";

        let a_tag = NEW("A", {
            "class": "md-content-a",
            "onclick": "goto_title_of_mdcontent__callback_mdcontent(this);"
        });
        a_tag.innerHTML = title_data[i][1]

        let div = NEW("DIV", {
            "class": "md-content-label",
            "data-level": title_data[i][0],
            "data-status": "unfolded",
            "data-id": i
        });

        div.appendChild(button);
        div.appendChild(a_tag);

        md_content.appendChild(div);

        window.mdcontent_label_state.push(["open"]);
    }
}


// 搜寻并跳转至a_tag对应的标题位置
function goto_title_of_mdcontent__callback_mdcontent(a_tag) {
    let div = a_tag.parentElement;
    let div_id = Number(div.getAttribute("data-id"));

    let mainarea = ID("main-area");
    let targetrect = CLASS("mdtag-h")[div_id].getBoundingClientRect();
    mainarea.scrollTo(0, mainarea.scrollTop + targetrect.y);
}

// 目录中的label前面的按钮按下去时的回调函数
// 通过改变label和label父div的data-status
// 来切换样式，即改变样式
function change_btn_status__callback_mdcontent(btn) {
    if (btn.getAttribute("data-status") == "unfolded") {
        btn.setAttribute("data-status", "folded");
        btn.parentElement.setAttribute("data-status", "folded");
    } else if (btn.getAttribute("data-status") == "folded") {
        btn.setAttribute("data-status", "unfolded");
        btn.parentElement.setAttribute("data-status", "unfolded");
    }
}

// window.mdcontent_label_state : [ [status, ele...], [...],... ]

// 展开/折叠md_content_label
function fold_mdcontent_label__callback_mdcontent(md_content_label) {
    let this_level = Number(md_content_label.getAttribute("data-level"));
    let this_id = Number(md_content_label.getAttribute("data-id"));

    if (window.mdcontent_label_state[this_id][0] == "closed") {              // to open
        let cursor = md_content_label;
        for (let i = 1; i < window.mdcontent_label_state[this_id].length; i++) {
            cursor.insertAdjacentElement("afterend", window.mdcontent_label_state[this_id][i]);
            cursor = cursor.nextElementSibling;
        }
        window.mdcontent_label_state[this_id] = window.mdcontent_label_state[this_id].slice(0, 1);
        window.mdcontent_label_state[this_id][0] = "open"
    } else if (window.mdcontent_label_state[this_id][0] == "open") {         // to close
        let cursor = md_content_label;
        let md_content = ID("md-content");
    
        cursor = cursor.nextElementSibling;
        while (true) {
            if (!cursor) break;
            if (Number(cursor.getAttribute("data-level")) > this_level) {
                window.mdcontent_label_state[this_id].push(cursor);
                let next_tmp = cursor.nextElementSibling;
                md_content.removeChild(cursor);
                cursor = next_tmp;
            } else {
                break;
            }
        }
        window.mdcontent_label_state[this_id][0] = "closed";
    }
}
