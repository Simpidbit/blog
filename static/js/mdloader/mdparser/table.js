// 渲染表格
function __markdown_table(raw) {
    let tarr = raw.split("\n");
    // 检查是否有表格存在
    // 并保存每一张表格的开始行标和结束行标

    let tables = [];
    let table_column_number = 0;
    let table_exist_flag = 0;
    for (let i = 0; i < tarr.length; i++) {
        let current_line_vertag_number = 0;
        try {
            current_line_vertag_number = tarr[i].match(/\|/g).length;
        } catch (error) {
            table_exist_flag = 0;
            table_column_number = 0;
            continue;
        }
        if (current_line_vertag_number > 1) {       // |数大于等于2
            if (table_column_number == current_line_vertag_number - 1) {
                                            // 表列数 = 此行 | 数-1
                if (!table_exist_flag) {        // 表本不存在，建一个新表
                    table_exist_flag = 1;

                    // 开始记录表的每行索引
                    tables.push([table_column_number, i-1, i]);
                } else {                        // 表本来就存在，继续记录
                    tables[tables.length - 1].push(i);
                }


            } else {                        // 表列数 ≠ 此行 | 数-1
                // 更新表列数，等待表出现
                table_column_number = current_line_vertag_number - 1;
            }
        }
    }


    // 储存表数据
    let tables_data = [];

    // 开始渲染每一张表
    for (let i = 0; i < tables.length; i++) {
        // 渲染第 i 张表
        let current_table = tables[i];

        // 首先获取表列数
        let table_column_number = current_table[0];

        // 获取表数据，将表信息(tables)写入每张表表数据的0位置
        // curtab_data[0]: [表列数, [...表位置]]
        let curtab_data = [];
        curtab_data.push([current_table[0], current_table.slice(1)]);
        for (let k = 1; k < current_table.length; k++) {
            let pieces = tarr[current_table[k]].split("|");
            pieces.shift();     // 掐头 ""
            pieces.pop();       // 去尾 ""
            for (let m = 0; m < pieces.length; m++) {
                pieces[m] = pieces[m].trim();
            }
            curtab_data.push(pieces);
        }

        tables_data.push(curtab_data);
    }


// 表数据采集完成，开始写表
    // 先把原来的表所在地全都删除，每张表只留一个占位符
    for (let i = 0; i < tables_data.length; i++) {      // 第 i 张表
        let curtab_data = tables_data[i];
        // Step1. 把所在行全部变成占位字符串 \x01TABLE{i}
        for (let k = 0; k < curtab_data[0][1].length; k++) {
            tarr[curtab_data[0][1][k]] = "\x01TABLE" + i;
        }
    }



        // Step2. 把连续的占位符收缩为1个
    let curlen = tarr.length;
    for (let i = 1; i < curlen; i++) {
        if (tarr[i].length >= 7
            && tarr[i-1].length >= 7
            && tarr[i].slice(0, 6) == "\x01TABLE"
            && tarr[i - 1].slice(0, 6) == "\x01TABLE") {
            tarr.splice(i, 1);
            curlen--;
            i--;
        }
    }

    // 然后构建表HTML，并把表HTML写入对应的占位符上
    for (let i = 0; i < tables_data.length; i++) {      // 第 i 张表
        let curtab_data = tables_data[i];
        let table_ele = NEW("TABLE", { "class": "mdtag-table" });


        // 这里处理表的对齐方式
        let aligns = [];        // 保存对齐字符串
        if (curtab_data.length >= 3) {
            for (let m = 0; m < curtab_data[0][0]; m++) {
                let align_code = curtab_data[2][m];
                if (align_code[0] == ":"
                    && align_code[align_code.length - 1] == ":"
                    && align_code.slice(1, align_code.length - 1) == '-'.repeat(align_code.length - 2)) {
                    aligns.push("center");
                } else if (align_code[align_code.length - 1] == ":"
                    && align_code.slice(0, align_code.length - 1) == '-'.repeat(align_code.length - 1)) {
                    aligns.push("right");
                } else {
                    aligns.push("left");
                }
            }
        }

        // 写表头
        let tr = NEW("TR");
        for (let k = 0; k < curtab_data[0][0]; k++) {
            let th = NEW("TH");
            th.innerHTML = curtab_data[1][k];
            th.style.textAlign = aligns[k];
            tr.appendChild(th);
        }
        table_ele.appendChild(tr);

        // 写表数据
        if (curtab_data.length >= 4) {
            for (let k = 3; k < curtab_data.length; k++) {
                // curtab_data 第 k 个元素
                let tr = NEW("TR");
                for (let m = 0; m < curtab_data[0][0]; m++) {
                    // curtab_data 第 k 个元素对应的行的第 m 列
                    let td = NEW("TD");
                    td.innerHTML = curtab_data[k][m];
                    td.style.textAlign = aligns[m];
                    tr.appendChild(td);
                }
                table_ele.appendChild(tr);
            }
        }

        // 写入占位符
        for (let k = 0; k < tarr.length; k++) {
            if (tarr[k].length >= 7
                && tarr[k].slice(0, 6) == "\x01TABLE") {
                if (Number(tarr[k].substr(6)) == i) {
                    try {
                        tarr[k] = "<div class=\"mdtag-table-container\"><table class=\"mdtag-table\">" + table_ele.getHTML() + "</table></div>";
                    } catch {    // firefox
                        tarr[k] = "<div class=\"mdtag-table-container\"><table class=\"mdtag-table\">" + table_ele.outerHTML + "</table></div>";
                    }
                }
            }
        }
    }


    let ret = "";
    for (let k = 0; k < tarr.length; k++) {
        if (k != tarr.length - 1) {
            ret += tarr[k] + '\n';
        } else {
            ret += tarr[k];
        }
    }


    return ret;
}
