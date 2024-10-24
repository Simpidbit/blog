// 扫描页面中的.mdtag-h
// 并写入html_title_digest
// html_title_digest: 
//  [
//      [第几级标题, 标题内容],
//      [第几级标题, 标题内容],
//      [第几级标题, 标题内容],
//      ....
//  ]
// 依据html_title_digest中的数据
// 构建md-content组件并写入左侧边栏
function render_mdcontent_from_globaldata__interface_mdcontent() {
    let html_title_digest = [];
    let titles = CLASS("mdtag-h");
    for (let k = 0; k < titles.length; k++) {
        html_title_digest.push([
            Number(titles[k].tagName.substr(1)),
            titles[k].innerHTML
        ]);
    }

    render_foldtree_to_ele_from_globaldata__interface_foldtree(
        html_title_digest,          ID("md-content"),       "md-content-tree",
        { 
            "class": "md-content-button" 
        },
        {
            "class": "md-content-a",
            "onclick": "goto_title_of_mdcontent__callback_mdcontent(this);"
        },
        {
            "class": "md-content-label"
        }, true
    );
}


// 搜寻并跳转至a_tag对应的标题位置
function goto_title_of_mdcontent__callback_mdcontent(a_tag) {
    let div = a_tag.parentElement;
    let div_id = Number(div.getAttribute("data-id"));

    let mainarea = ID("main-area");
    let targetrect = CLASS("mdtag-h")[div_id].getBoundingClientRect();
    mainarea.scrollTo(0, mainarea.scrollTop + targetrect.y);
}
