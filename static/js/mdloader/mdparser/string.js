function combine_space(s) {
    // 合并连续多个空格
    let replaced = s.replaceAll("  ", ' ');
    while (replaced != s) {
        s = replaced;
        replaced = s.replaceAll("  ", ' ');
    }
    return replaced;
}
