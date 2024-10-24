// 负责markdown代码块的渲染
function __markdown_code(raw) {
    raw = parse_partof_md_to_html__local_markdown(raw, /```\w*?\n[^]*?```/g, s => {
        let begin_index = s.search(/(?<=```\w*?\n)[^]*?```/g);
        let language = s.match(/(?<=```)\w*?(?=\n)/g)[0]; //`
        let content = s.slice(begin_index, s.length - 1 - 2);
        s = __markdown_escape_HTML(s);
        s = __markdown_escape_raw(s);
        if (language == "mermaid") {
            return "<pre class=\"mdtag-mermaid\" data-codetype=\"" + language + "\">" + content + "</pre>";
        } else  {
            content = s.slice(begin_index, s.length - 1 - 2);
            return "<div class=\"mdtag-code-container\"><code class=\"mdtag-code\" data-codetype=\"" + language + "\">" + content + "</code></div>";
        }
    });

    // 行内代码`aowief`
    // 应放在代码块渲染之后
    raw = parse_partof_md_to_html__local_markdown(raw, /`[^]*?`/g, s => {

        // 这一行是为了修复多行quote被内联code包裹时，符号 > 未能消去的bug
        s = s.replaceAll(/\n\ *> /g, "\n");

        s = __markdown_escape_raw(s);
        return "<div class=\"mdtag-inline-code\">" + s.slice(1, s.length - 1) + "</div>";
    });

    return raw;
}
