window.__markdown_raw_protect_table = [
    ['#', '\x01'], ['-', '\x02'],
    ['|', '\x03'], ['[', '\x04'],
    [']', '\x05'], ['(', '\x06'],
    [')', '\x07'], [':', '\x08'],
    ['{', '\x10'], ['}', '\x11'],
    ['*', '\x12'], ['~', '\x13'],
    ['$', '\x14'], ['%', '\x15'],
    ['^', '\x16'], ['@', '\x17'],
    ['!', '\x18'], ['`', '\x19']
];


function __markdown_escape_HTML(s) {
    s = s.replaceAll("&", "&amp;");
    s = s.replaceAll("<", "&lt;");
    s = s.replaceAll(">", "&gt;");
    s = s.replaceAll("\"", "&quot;");
//    s = s.replaceAll("\'", "&39;");
    return s;
}


function __markdown_escape_raw(raw) {
    // 原始代码保护
    for (let i = 0; i < window.__markdown_raw_protect_table.length; i++) {
        raw = raw.replaceAll(
            window.__markdown_raw_protect_table[i][0],
            window.__markdown_raw_protect_table[i][1]
        );
    }

    return raw;
}

function __markdown_unescape_raw(raw) {
    // 保护代码还原
    for (let i = 0; i < window.__markdown_raw_protect_table.length; i++) {
        raw = raw.replaceAll(
            window.__markdown_raw_protect_table[i][1],
            window.__markdown_raw_protect_table[i][0]
        );
    }

    return raw;
}
