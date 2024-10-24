function __markdown_title(raw) {
    console.log("NOW TITLE########################");
    raw = parse_partof_md_to_html__local_markdown(raw, /(?<=((^|\n)\ *))(?<!#)#{1,1}\ +?[^]*?\r?(\n|$)/g, function(s) {
        return "<h1 class=\"mdtag-h\">" + s.substr(1) + "</h1>";
    });

    raw = parse_partof_md_to_html__local_markdown(raw, /(?<=((^|\n)\ *))(?<!#)#{2,2}\ +?[^]*?\r?(\n|$)/g, function(s) {
        return "<h2 class=\"mdtag-h\">" + s.substr(2) + "</h2>";
    });

    raw = parse_partof_md_to_html__local_markdown(raw, /(?<=((^|\n)\ *))(?<!#)#{3,3}\ +?[^]*?\r?(\n|$)/g, function(s) {
        return "<h3 class=\"mdtag-h\">" + s.substr(3) + "</h3>";
    });
    raw = parse_partof_md_to_html__local_markdown(raw, /(?<=((^|\n)\ *))(?<!#)#{4,4}\ +?[^]*?\r?(\n|$)/g, function(s) {
        return "<h4 class=\"mdtag-h\">" + s.substr(4) + "</h4>";
    });

    raw = parse_partof_md_to_html__local_markdown(raw, /(?<=((^|\n)\ *))(?<!#)#{5,5}\ +?[^]*?\r?(\n|$)/g, function(s) {
        return "<h5 class=\"mdtag-h\">" + s.substr(5) + "</h5>";
    });

    return raw;
}
