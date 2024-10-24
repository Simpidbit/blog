/**
 * 判断给定的字符串是否为开始标签、结束标签或自闭合标签
 * 如果是开始标签，返回 "begin"
 * 如果是结束标签，返回 "end"
 * 如果是自闭合标签，返回 "self"
 * 如果是未知类型的标签，打印警告并返回 "unknown"
 *
 * @param {string} tagstr - 要检查的字符串
 * @returns {string} - 表示标签类型的字符串
 */
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


/**
 * 分析给定的 HTML 片段，提取出所有的标签并打印到控制台
 *
 * @param {string[]} ret - 一个字符串数组，这里假设 ret[0] 包含要分析的 HTML 内容
 * @param {string} raw - 原始的 HTML 内容
 * @returns {string} raw - 返回被修改后的 HTML 内容
 */
function __markdown_ul_li_single_li(ret, raw) {
    let offset = ret.index;
    let tag_reg = /\<\/?\w+([^\<\>]+)?\>/g;
    let tag_ret = null;
    tag_ret = tag_reg.exec(ret[0]);

    let unend_tag_number = 0;
    let last_tag_ret = tag_ret;
    while (tag_ret != null) {
        switch (__markdown_ul_li_tag_begin_or_end(tag_ret[0])) {
            case "begin":
                unend_tag_number++;
                break;
            case "end":
                unend_tag_number--;
                break;
            case "unknown":
                break;
        }
        last_tag_ret = tag_ret;
        tag_ret = tag_reg.exec(ret[0]);
    }
    if (unend_tag_number > 0) {
        tag_reg.lastIndex = offset + last_tag_ret.index + last_tag_ret[0].length;
        // 往后直到unend_tag_number = 0
        while (true) {
            tag_ret = tag_reg.exec(raw);
            switch (__markdown_ul_li_tag_begin_or_end(tag_ret[0])) {
                case "begin":
                    unend_tag_number++;
                    break;
                case "end":
                    unend_tag_number--;
                    break;
                case "unknown":
                    break;
            }
            if (unend_tag_number == 0) break;
        }
        // 之间的\n全部换成\x1d
        for (let i = offset + last_tag_ret.index + last_tag_ret[0].length - 1;
                 i < tag_ret.index; i++) {
            if (raw[i] == '\n') {
                raw = raw.slice(0, i) + '\x1d' + raw.substr(i + 1);
            };
        }
    }

    return raw;
}


// 任务：把 - 后面能看成一个整体的节点的开始和结束之间的\n替换为\x1d
/**
 * 对给定的原始 Markdown 文本进行处理，为所有的 HTML 标签进行标记，并对文本中的每个列表项（li）进行单独处理
 *
 * @param {string} raw - 原始 Markdown 文本
 * @return {string} - 处理后的 Markdown 文本
 */
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

