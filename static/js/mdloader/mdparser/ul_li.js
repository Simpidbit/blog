function __markdown_ul_li_tag_begin_or_end(tagstr) {
    if (/\<\w+([^\<\>\/]+)?\>/g.test(tagstr)) {
        return "begin";
    } else if (/\<\/\w+([^\<\>\/]+)?\>/g.test(tagstr)) {
        return "end";
    } else if (/\<\w+([^\<\>]+)?\/\>/g.test(tagstr)) {
        return "self";
    } else {
        console.warn(`@__markdown_ul_li_tag_begin_or_end(${tagstr}) Unknown tag type: ${tagstr}`);
        return "unknown";
    }
}


function __markdown_ul_li_single_li(ret, raw) {
    console.log("分析: ", ret[0]);
    let tag_reg = /\<\/?\w+([^\<\>]+)?\>/g;
    let tag_ret = null;
    tag_ret = tag_reg.exec(ret[0]);


    while (tag_ret != null) {
        console.log(tag_ret[0]);
        tag_ret = tag_reg.exec(ret[0]);
    }


    return raw;
}


// 任务：把 - 后面能看成一个整体的节点的开始和结束之间的\n替换为\x1d
function __markdown_ul_li_patch_entire(raw) {
    // 首先给所有的html标签打上label

    let ul_reg = /(?<=(^|\n))\ *?-\ +?[^]*?(?=($|\n))/g;
    
    let ret = null;
    ret = ul_reg.exec(raw);
    while (ret != null) {
        // 这里处理匹配到的ul_li行
        raw = __markdown_ul_li_single_li(ret, raw);
        ret = ul_reg.exec(raw);
    }

    return raw;
}

// 负责渲染无序列表
function __markdown_ul_li(raw) {
    let ret = "";

    raw = __markdown_ul_li_patch_entire(raw);

    let sentences = raw.split("\n");
    let space_counter = [];

    // ul_li 分层
    let reg = /^\ *?-\ +?/;
    for (let i = 0; i < sentences.length; i++) {
        if (reg.test(sentences[i])) {
            let space_reg = /^\ *?-/;
            let li_level = sentences[i].match(space_reg)[0].length - 1;

            let counter_index = space_counter.findIndex(e => e[0] == li_level);
            if (counter_index == -1) {
                space_counter.push([li_level, i]);
            } else {
                space_counter[counter_index].push(i);
            }
        }
    }

    // 由外层向内层渲染
    // 找到最少space的，渲染后调高
    let level = 0;
    for (let k = 0; k < space_counter.length; k++) {
        let min_space_number = Number.MAX_VALUE;
        for (let i = 0; i < space_counter.length; i++) {
            if (space_counter[i][0] < min_space_number) {
                min_space_number = space_counter[i][0];
            }
        }
        let min_space_index = space_counter.findIndex(e => {
            if (e[0] == min_space_number) {
                e[0] = Number.MAX_VALUE;
                return true;
            }
        });
        for (let i = 1; i < space_counter[min_space_index].length; i++) {
            let current_sentence_index = space_counter[min_space_index][i];
            sentences[current_sentence_index] = sentences[current_sentence_index].replace(/^\ *?-\ +/, "<li data-level=" + level + " class=\"mdtag-li\">");
            sentences[current_sentence_index] += "</li>"
        }
        level++;
    }

    // 合体
    for (let i = 0; i < sentences.length; i++) {
        if (i == sentences.length - 1) {
            ret += sentences[i];
            break;
        } else {
            ret += sentences[i];
            ret += '\n';
        }
    }
    return ret.replace('\x1d', '\n');
}

