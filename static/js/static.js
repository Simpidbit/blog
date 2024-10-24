function ID(ele_id) {
    return document.getElementById(ele_id);
}

function CLASS(ele_class) {
    return document.getElementsByClassName(ele_class);
}

function TAG(ele_tag) {
    return document.getElementsByTagName(ele_tag);
}

function NEW(tagname, attributes = {}) {
    let tag = document.createElement(tagname);
    for (let key in attributes) {
        tag.setAttribute(key, attributes[key]);
    }
    return tag;
}
