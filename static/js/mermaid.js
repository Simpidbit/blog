mermaid.initialize({ startOnLoad: false });

// 渲染mermaid
// 核心就是把innerHTML变成innerText，
// 因为innerHTML会自动转义掉>，
// 如果>被转义了，就会变成&gt;，直接语法错误
// innerText不会自动转义
// 输入：要解析mermaid语法的节点组成的数组
// 输出：自动把这些节点变成mermaid图
function render_all_elements_to_mermaid__interface_mermaid(eles) {
    for (let i = 0; i < eles.length; i++) {
        eles[i].innerHTML = eles[i].innerText;
    }
    mermaid.run({nodes:eles});
}
