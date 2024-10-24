window.onload = function() {
    // 通过地址栏地址，
    // 判断是从根目录开始的还是从别的目录开始的
    let pathque = get_path_queue__interface_pathque();
    render_navigator_from_JSON__interface_navigator();
    switch (pathque.length) {
        case 0:     // 根目录
            update_markdown_to_main_area__interface_loader("/index.md", true);
            break;
        case 1:
            if (pathque[0] == "root") {
                async_try_until_ok__interface_wait(goto_main_index__callback_navigator, 0);
            }
            break;
        default:
            pathque.shift();        // 弃去 "root"
            update_markdown_to_main_area__interface_loader(get_pathname_from_path_queue__interface_pathque(pathque), true);
    }

    register_event_listener__interface_event();


    // 非阻塞式引入较大的script
    setTimeout(function() {
        let script = NEW("SCRIPT", {
            "src": "/static/js/external_MathJax/es5/tex-mml-chtml.js",
            "onload": "async_try_until_ok__interface_wait(MathJax.typeset, 200);"
        });
        document.head.appendChild(script);
    }, 5);
}
