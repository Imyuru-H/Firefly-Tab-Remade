// 获取元素的绝对位置坐标（相对于页面左上角）
function getElementPagePosition(element) {
    // 计算x坐标
    var actualLeft = element.offsetLeft;
    var current = element.offsetParent;
    while (current !== null) {
        actualLeft += current.offsetLeft;
        current = current.offsetParent;
    }
    // 计算y坐标
    var actualTop = element.offsetTop;
    current = element.offsetParent;
    while (current !== null) {
        actualTop += (current.offsetTop + current.clientTop);
        current = current.offsetParent;
    }
    // 返回结果
    return { x: actualLeft, y: actualTop };
}

(function () {
    // 定义边框元素
    var l = document.getElementById("border_left"),
        r = document.getElementById("border_right"),
        page = document.getElementById("page");

    // 定义内容元素
    var content = document.getElementById("content");
    var text = document.getElementById("text");
    var title = document.getElementById("title");
    var ref = document.getElementById("ref");

    setInterval(function () {
        // 计算内容元素的位置
        var ct_lt = getElementPagePosition(text),
            ct_rb = { x: ct_lt.x + text.offsetWidth, y: ct_lt.y + text.offsetHeight };

        // 计算标题元素的位置
        var tt_lt = getElementPagePosition(title),
            tt_rb = { x: tt_lt.x + title.offsetWidth, y: tt_lt.y + title.offsetHeight };

        // 计算编号元素的位置
        var rf_lt = getElementPagePosition(ref),
            rf_rb = { x: rf_lt.x + ref.offsetWidth, y: rf_lt.y + ref.offsetHeight };

        var lpos = getElementPagePosition(l),
            rpos = getElementPagePosition(r);
        
        var ldx = tt_lt.x - lpos.x,
            ldy = tt_lt.y - lpos.y - 40,
            rdx = tt_rb.x - rpos.x - r.offsetWidth,
            rdy = rf_rb.y - rpos.y + 40;

        // 计算并改变边框位置
        content.style.width = `${document.body.offsetWidth}`;
        l.style.left = `${text.offsetWidth * 0}px`;
        r.style.right = `${text.offsetWidth * 0}px`;
        l.style.transform = `translate(${ldx}px,${ldy}px) scale(275%)`;
        r.style.transform = `translate(${rdx}px,${rdy}px) scale(-275%)`;
    }, 1000 / 60);
})();