function register_event_listener__interface_event() {
    let main_area = ID("main-area");
    document.addEventListener('keydown', function(event) {
        switch (event.key) {
            case 'k':
                main_area.scrollBy(0, -200);
                break;
            case 'd':
                main_area.scrollBy(0, -200);
                break;
            case 'm':
                main_area.scrollBy(0, -1000);
                break;
            case 'c':
                main_area.scrollBy(0, -1000);
                break;
            case 'j':
                main_area.scrollBy(0, 200);
                break;
            case ' ':
                main_area.scrollBy(0, 200);
                break;
            case 'f':
                main_area.scrollBy(0, 200);
                break;
            case 'n':
                main_area.scrollBy(0, 1000);
                break;
            case 'v':
                main_area.scrollBy(0, 1000);
                break;
            case 'Escape':
                ID("goto-main-content").click();
                break;
            case 'r':
                ID("goto-main-content").click();
                break;
            case 'b':
                ID("goto-main-content").click();
                break;
            default: console.log(event.key);
        }
    });
}
