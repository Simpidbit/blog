/*
	此函数负责构建foldtree.
	参数：
		list_data: 以列表的形式顺序列出所有label, 格式：[ [逻辑层级, 内容], [逻辑层级, 内容], ... ]
		ele: 这棵树写到哪个元素上
		key: 树的名字，关系到树的临时数据存放
		btn_attributes: 折叠按钮的属性，键值对的value为函数时，键对应的值为函数的返回值，函数传入参数(list_data, 此时list_data的索引位置)，下同
		a_attributes: 折叠按钮后面链接（内容）的属性
		div_attributes: 一对超链接和按钮组成的label的属性
		whether_clear: 布尔值，是否清空 window.foldtree_isfold_data[key] 的数据
        tabpx: 默认值30, 控制foldtree前面一个缩进的长度, 单位是px
	此函数将会:
		将这棵树的折叠数据写入 window.foldtree_isfold_data[key][1]
		将构建出来的foldtree写入ele元素中
		将ele写入 window.foldtree_isfold_data[key][0]
*/
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


/*
    foldtree中，每个条目前面的小按钮被点击时调用的回调函数
    参数:
        btn: 调用这个函数的按钮
    此函数将会:
        切换被点击的按钮的相关样式
*/
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
/*
    foldtree中，每个条目(目录型, 即有子条目的)被点击时的回调函数
    参数:
        foldtree_label: 谁调用的这个回调函数
        key: 保存foldtree数据的树的名字, 意义同render_foldtree_to_ele_from_globaldata__interface_foldtree()里的key
    此函数将会:
        切换被点击条目的展开/折叠状态
        本来折叠的切换成展开，本来展开的切换成折叠
*/
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
