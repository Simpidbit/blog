    // markdown内联式超链接
    // [链接文本](链接地址)
function __markdown_inline_url(raw) {
    return parse_partof_md_to_html__local_markdown(raw, /(?<!\!)\[[^\[\]]+\]\ ?\([^]+?\)/g,
        s=>{
            let pieces = [];
            if (s.split("](").length == 1) {
                pieces = s.split("] (");
            } else {
                pieces = s.split("](");
            }

            text = pieces[0].substr(1);
            url = pieces[1].slice(0, pieces[1].length - 1);

            return `<a class=\"mdtag-a\" href=\"${url}\" target=\"_blank\">${text}</a>`;
    });
}

function __markdown_refer_url(raw) {
    // markdown引用式超链接
    let urldefined = [];
    raw = parse_partof_md_to_html__local_markdown(raw, /(?<!\!)\[[^\[\]]+\]\ ?:\ ?(\w+:\/\/)?((\w+\.)+\w+(:[0-9]+)?)(\/[^\/\ \n\r]+?)*\/?(?=(\ |\n|\r|$))/g,
        s => {
            let pieces = s.split(']');
            let identifier = pieces[0].substr(1);

            pieces[1] = pieces[1].trim();
            if (pieces[1][0] == ":") {
                pieces[1] = pieces[1].substr(1);
                pieces[1] = pieces[1].trim();
            }
            let url = pieces[1];
            urldefined.push([identifier, url]);

            return "";
    });

    // 接上：markdown引用式超链接
    raw = parse_partof_md_to_html__local_markdown(raw, /\[[^\[\]]+\]\ ?\[[^\[\]]+\]/g,
        s => {
            let pieces = [];
            if (s.split("][").length == 1) {
                pieces = s.split("] [");
            } else {
                pieces = s.split("][");
            }
            let text = pieces[0].substr(1);
            let identifier = pieces[1].slice(0, pieces[1].length - 1);

            for (let k = 0; k < urldefined.length; k++) {
                if (urldefined[k][0] == identifier) {
                    return `<a class=\"mdtag-a\" href=\"${urldefined[k][1]}\" target=\"_blank\">${text}</a>`;
                }
            }
            return s;
    });

    return raw;
}


function __markdown_naked_url(raw) {
    pieces = [""];
    for (let i = 0; i < raw.length; i++) {
        if (raw[i] != '\n' && raw[i] != '\ ') {
            pieces[pieces.length - 1] += raw[i];
        } else {
            pieces.push(raw[i]);
        }
    }

    for (let i = 0; i < pieces.length; i++) {
        let res = pieces[i].match(/(?<=(\ |\n|^|\r))(\w+:\/\/)((\w+\.)+\w+(:[0-9]+)?)(\/[^\/\ \n\r]+?)*\/?(?=(\ |\n|\r|$))/g);
        if (res == null) {
            continue;
        } else {
            if ((!res[0].match(/\w+:\/\//g))) {
                pieces[i] = pieces[i].replace(res[0], "<a class=\"mdtag-a\" href=\"http://" + res[0] + "\" target=\"_blank\">" + res[0] + "</a>");
            } else {
                pieces[i] = pieces[i].replace(res[0], "<a class=\"mdtag-a\" href=\"" + res[0] + "\" target=\"_blank\">" + res[0] + "</a>");
            }
        }
    }

    let ret = "";
    for (let k = 0; k < pieces.length; k++) {
        ret += pieces[k];
    }
    return ret;
}
