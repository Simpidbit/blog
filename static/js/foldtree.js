// 依据list_data中的数据
// 构建md-content组件并写入ele
// 折叠/展开数据放在window.foldtree_isfold_data[key][1]里
// window.foldtree_isfold_data[key][0] 装着的是ele
window.foldtree_isfold_data = {};
function render_foldtree_to_ele_from_globaldata__interface_foldtree (
    list_data,          ele,            key,
    btn_attributes,     a_attributes,   div_attributes,
    whether_clear,      tabpx = 30)
{
    if (whether_clear) {
        window.foldtree_isfold_data[key] = [null, null];
        window.foldtree_isfold_data[key][0] = ele;
        window.foldtree_isfold_data[key][1] = [];
    } else {
        window.foldtree_isfold_data[key][0] = ele;
    }

    for (let i = 0; i < list_data.length; i++) {

        let button = NEW("BUTTON", {
            "onclick": `change_btn_status__callback_mdcontent(this);fold_foldtree_label__callback_mdcontent(this.parentElement, \"${key}\");`,
            "data-status": "unfolded"
        });
        button.innerHTML = "";
        let keys = Object.keys(btn_attributes);
        for (let k = 0; k < keys.length; k++) {
            if (btn_attributes[keys[k]] instanceof Function) {
                button.setAttribute(keys[k], btn_attributes[keys[k]](i, list_data));
            } else {
                if (keys[k] == "btn-text") {
                    button.innerHTML = btn_attributes[keys[k]];
                } else {
                    button.setAttribute(keys[k], btn_attributes[keys[k]]);
                }
            }
        }

        let a_tag = NEW("A");
        a_tag.innerHTML = list_data[i][1]
        keys = Object.keys(a_attributes);
        for (let k = 0; k < keys.length; k++) {
            if (a_attributes[keys[k]] instanceof Function) {
                a_tag.setAttribute(keys[k], a_attributes[keys[k]](i, list_data));
            } else {
                a_tag.setAttribute(keys[k], a_attributes[keys[k]]);
            }
        }

        let div = NEW("DIV", {
            "data-level": list_data[i][0],
            "data-status": "unfolded",
            "data-id": i
        });
        div.style.paddingLeft = `${tabpx * list_data[i][0]}px`;
        keys = Object.keys(div_attributes);
        for (let k = 0; k < keys.length; k++) {
            if (div_attributes[keys[k]] instanceof Function) {
                div.setAttribute(keys[k], div_attributes[keys[k]](i, list_data));
            } else {
                div.setAttribute(keys[k], div_attributes[keys[k]]);
            }
        }

        

        div.appendChild(button);
        div.appendChild(a_tag);

        ele.appendChild(div);

        window.foldtree_isfold_data[key][1].push(["open"]);
    }
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

// window.foldtree_isfold_data[key]: [ [status, ele...], [...],... ]

// 展开/折叠 foldtree_label
function fold_foldtree_label__callback_mdcontent(foldtree_label, key) {
    let this_level = Number(foldtree_label.getAttribute("data-level"));
    let this_id = Number(foldtree_label.getAttribute("data-id"));

    if (window.foldtree_isfold_data[key][1][this_id][0] == "closed") {              // to open
        let cursor = foldtree_label;
        for (let i = 1; i < window.foldtree_isfold_data[key][1][this_id].length; i++) {
            cursor.insertAdjacentElement("afterend", window.foldtree_isfold_data[key][1][this_id][i]);
            cursor = cursor.nextElementSibling;
        }
        window.foldtree_isfold_data[key][1][this_id] = window.foldtree_isfold_data[key][1][this_id].slice(0, 1);
        window.foldtree_isfold_data[key][1][this_id][0] = "open"
    } else if (window.foldtree_isfold_data[key][1][this_id][0] == "open") {         // to close
        let cursor = foldtree_label;
        let md_content = window.foldtree_isfold_data[key][0];
    
        cursor = cursor.nextElementSibling;
        while (true) {
            if (!cursor) break;
            if (Number(cursor.getAttribute("data-level")) > this_level) {
                window.foldtree_isfold_data[key][1][this_id].push(cursor);
                let next_tmp = cursor.nextElementSibling;
                md_content.removeChild(cursor);
                cursor = next_tmp;
            } else {
                break;
            }
        }
        window.foldtree_isfold_data[key][1][this_id][0] = "closed";
    }
}
