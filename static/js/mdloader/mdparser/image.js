function __markdown_image(raw) {
    // markdown 图片
    return parse_partof_md_to_html__local_markdown(raw, /\!\[[^\[\]]+\]\ ?\([^]+?\)/g,
        s=>{
            let pieces = [];
            if (s.split("](").length == 1) {
                pieces = s.split("] (");
            } else {
                pieces = s.split("](");
            }

            text = pieces[0].substr(2);
            url = pieces[1].slice(0, pieces[1].length - 1);

            return "<img class=\"mdtag-img\" src=\"" + url + "\" alt=\"" + text + "\" />"
    });
}
