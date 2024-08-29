// 输入数据：内部自动获取 地址栏中的path字符串
// 输出：以返回值的形式输出
// 返回值：一个数组，索引从低到高依次是path的低层到高层
// 例如，地址栏 https://simpidbit.site/root/     返回 ['root']
//              https://simpidbit.site/root/test/test.md      返回 ['root', 'test', 'test.md']
//              https://simpidbit.site      返回 []
function get_path_queue__interface_pathque() {
    let pathname = window.location.pathname;

    // 如果正处于根目录，直接返回空数组
    if (pathname == '/') return [];

    // 预处理: 如果最后一位是"/"，直接截掉
    if (pathname[pathname.length - 1] == '/') {
        pathname = pathname.substr(0, pathname.length - 1);
    }

    let path_queue = pathname.split("/");
    path_queue.shift();     // 第一个元素是""，掐掉

    return path_queue;
}

// 输入数据：pathque
// 输出：以返回值的形式输出
// 返回值：pathque对应的pathname
function get_pathname_from_path_queue__interface_pathque (pathque) {
    let pathname = "";
    if (pathque.length == 0) return "/";
    for (let i = 0; i < pathque.length; i++) {
        pathname += `/${pathque[i]}`;
    }
    return pathname;
}
