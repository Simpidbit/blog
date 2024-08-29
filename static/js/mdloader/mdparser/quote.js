// 渲染引用
function __markdown_quote(raw) {
    let ret = "";
    let sentences = raw.split("\n");
    let regarr = [
        /^\ *>\ +/,
        /^(\ *>){2}\ +/,
        /^(\ *>){3}\ +/,
        /^(\ *>){4}\ +/,
        /^(\ *>){5}\ +/
    ];

    let last_level = -1;
    let div_counter = 0;
    let headhtml = "<div class=\"mdtag-quote" + last_level + "\">";
    let tailhtml = "</div>";
    for (let i = 0; i < sentences.length; i++) {
        let is_quote_flag = 0;
        for (let j = regarr.length - 1; j >= 0; j--) {
            if (regarr[j].test(sentences[i])) {
                // 此时 j 表示层数
                is_quote_flag = 1;
                sentences[i] = sentences[i].replace(regarr[j], "");

                if (j != last_level) {
                    headhtml = "<div class=\"mdtag-quote" + j + "\">";
                    sentences[i] = headhtml + sentences[i];
                    div_counter++;
                    last_level = j;
                }

                break;
            }
        }
        if (!is_quote_flag || i == sentences.length - 1) {      // quote断了
            for (let j = 0; j < div_counter; j++) {
                sentences[i] += tailhtml;
            }
            last_level = -1;
            div_counter = 0;
        }
    }


    for (let i = 0; i < sentences.length; i++) {
        if (i != sentences.length - 1) {
            ret += sentences[i] + "\n";
        } else {
            ret += sentences[i];
        }
    }

    return ret;
}
