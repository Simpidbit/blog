function __markdown_quote(raw) {
    let regarr = [
        /(?<=(\s+|^))(\ *>){1}\ +/,
        /(?<=(\s+|^))(\ *>){2}\ +/,
        /(?<=(\s+|^))(\ *>){3}\ +/,
        /(?<=(\s+|^))(\ *>){4}\ +/,
        /(?<=(\s+|^))(\ *>){5}\ +/
    ];

    // 第一阶段：将各行标记出level

    let lines = raw.split('\n');
    let line_quote_levels = __markdown_quote_mark_line_level(lines);

    // 第二阶段：根据标记出的level来渲染行
    let tagnumber = 0;
    for (let i = 0; i < lines.length; i++) {
        let current_level = line_quote_levels[i];
        let last_level = line_quote_levels[i - 1];
       

        if (current_level != 0) {// 有有效quotemark
            if (i == 0) {                   // 第一行就是有效quotemark，此时last_level = undefined
                lines[0] = lines[0].replace(
                    /(?<=(\ |^))(>\ *)+(\ |$)/,
                    `<div class=\"mdtag-quote${current_level - 1}\">`
                );
                tagnumber++;
                continue;
            }

            if (last_level == current_level) {  // level和上一行一样
                lines[i] = lines[i].replace(/(?<=(\ |^))(>\ *)+(\ |$)/, "");
            } else {                            // level和上一行不一样
                lines[i] = lines[i].replace(
                    /(?<=(\ |^))(>\ *)+(\ |$)/,
                    `<div class=\"mdtag-quote${current_level - 1}\">`
                );
                tagnumber++;
            }
        } else {                        // 无有效quotemark
            if (i == 0) {                   // 第一行，啥也不干
                continue;                   
            } else {                        // 不是第一行，要把尾巴补上，并重置各项数据
                lines[i - 1] = lines[i - 1] + "</div>".repeat(tagnumber);
                tagnumber = 0;
            }
        }
    }

    // 第三阶段，组装lines
    let ret = "";
    for (let i = 0; i < lines.length; i++) {
        if (i != lines.length - 1) {
            ret += lines[i] + '\n';
        } else {
            ret += lines[i];
        }
    }

    return ret;
}

/*
    返回值结构:
        [
            ...
            第一堆有效的连续quotemark出现几次,      // lines[i]
            ...
        ]
*/
function __markdown_quote_mark_line_level(lines) {
    let ret = [];
    let lastparse = null;
    let lineparse = null;
    for (let i = 0; i < lines.length; i++) {
        lineparse = __markdown_quote_mark_line_parse(lines[i]);
        if (/foldtree.js/.test(lines[i])) {
        }
        if (lineparse[0]) {         // 前面有别的字符
            if (lastparse != null && lastparse[0] && lastparse[1] != 0) {         // 上一个前面也有别的字符
                ret.push(0);
                // lastparse 一定要深拷贝
                lastparse = JSON.parse(JSON.stringify(lineparse));
                continue;
            } else {                    // 上一个前面没有别的字符
                ret.push(lineparse[1]);
            }
        } else {                    // 前面无别的字符
            ret.push(lineparse[1]);
        }

        // lastparse 一定要深拷贝
        lastparse = JSON.parse(JSON.stringify(lineparse));
    }

    return ret;
}

// [前面是否有别的字符, 第一次连续 > 出现几次]
function __markdown_quote_mark_line_parse(line) {
    line = combine_space(line);
    let pieces = line.split(' ');
    if (pieces[0] == '') pieces.shift();
    if (pieces[pieces.length - 1] == '') pieces.pop();

    let is_begin = -1;
    let has_divided_into_quotemark = false;
    let marknumber = 0;
    for (let i = 0; i < pieces.length; i++) {
        if (/^>+$/g.test(pieces[i])) {    // 是 >*n
            if (i == 0) {
                is_begin = true;
            }

            if (!has_divided_into_quotemark) {
                has_divided_into_quotemark = true;
            }

            marknumber += pieces[i].length;
        } else {                        // 其他字符
            if (i == 0) {
                is_begin = false;
            }

            if (has_divided_into_quotemark) {
                break;
            }
        }
    }
    return [!is_begin, marknumber];
}
