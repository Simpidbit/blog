// 负责处理reg相对应的markdown规则，具体处理由renderFunc决定
// renderFunc是一个函数对象，且必须有一个参数用于接收reg匹配到的字符串，
// 返回处理后的raw
function parse_partof_md_to_html__local_markdown(raw, reg, renderFunc) {
    let regresult = raw.match(reg);
    if (regresult == null) return raw;
    for (let i = 0; i < regresult.length; i++) {
        raw = raw.replace(regresult[i], renderFunc(regresult[i]));
    }
    return raw;
}


// markdown渲染的主函数
function parse_markdown_to_html__local_markdown(raw) {
    // 去除字符串开头和结尾的空格
    raw = raw.trim();


    // code，必须放在前面，对code内的特殊符号进行保护
    raw = __markdown_code(raw);


    // 引用渲染
    raw = __markdown_quote(raw);

    // 无序列表渲染
    raw = __markdown_ul_li(raw);
    raw = raw.replaceAll('\x1d', '\n');



    // markdown内联式超链接
    raw = __markdown_inline_url(raw);

    // markdown引用式超链接
    raw = __markdown_refer_url(raw);

    // markdown 图片
    raw = __markdown_image(raw);

    // 超链接（裸）渲染，必须在markdown超链接渲染之后
    raw = __markdown_naked_url(raw);

    // 表格渲染
    raw = __markdown_table(raw);

    // h1 ~ h5
    raw = __markdown_title(raw);

    // --- <hr />
    raw = parse_partof_md_to_html__local_markdown(raw, /\n\-\-\-/g, s => { return "<hr />" })


    // **字体加粗**
    raw = parse_partof_md_to_html__local_markdown(raw, /(?<!\*)\*\*[^]+?\*\*(?!\*)/g, s => { return `<b>${s.slice(2, s.length - 2)}</b>`; })

    // \n, must be the end
    raw = parse_partof_md_to_html__local_markdown(raw, /\n\ *?\n/g, s => { return "<br />"; });

    // \t, must be the end
    raw = parse_partof_md_to_html__local_markdown(raw, /\t/g, s => { return "&nbsp;".repeat(2); });

    // 连续多个空格, must be the end
    raw = parse_partof_md_to_html__local_markdown(raw, /\ \ +/g, s => {
        let ret = "";
        for (let i = s; i < s.length; i++) { ret += "&nbsp;"; }
        return ret;
    });

    // 还原受保护的特殊符号
    raw = __markdown_unescape_raw(raw);

    return raw;
}
