// 渲染引用
function __markdown_quote(raw) {
    let ret = "";
    let sentences = raw.split("\n");
    let regarr = [
        /(?<=\s+)(\ *>){1}\ +/,
        /(?<=\s+)(\ *>){2}\ +/,
        /(?<=\s+)(\ *>){3}\ +/,
        /(?<=\s+)(\ *>){4}\ +/,
        /(?<=\s+)(\ *>){5}\ +/
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
                sentences[i] = sentences[i].replace(regarr[j], "quote\x01quote");

                // 找到占位符所在的位置，并干掉占位符
                let sign_index = 0;
                for (let m = 0; m < sentences[i].length; m++) {
                    if (sentences[i].substr(m, 11) == "quote\x01quote") {
                        sign_index = m;
                        break;
                    }
                }
                sentences[i] = sentences[i].replace("quote\x01quote", "");

                if (j != last_level) {
                    headhtml = "<div class=\"mdtag-quote" + j + "\">";
                    sentences[i] = sentences[i].slice(0, sign_index) + headhtml + sentences[i].substr(sign_index);
                    div_counter++;
                    last_level = j;
                }

                break;
            }
        }
        if (!is_quote_flag || i == sentences.length - 1) {      // quote断了
            for (let j = 0; j < div_counter; j++) {
                sentences[i] = tailhtml + sentences[i];
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
