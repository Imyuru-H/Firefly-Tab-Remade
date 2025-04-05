let centerX, centerY;
let background, content;

function updateCenter() {
    centerX = document.body.offsetWidth / 2;
    centerY = document.body.offsetHeight / 2;
}

function getMousePos(event) {
    const e = event || window.event;
    return { x: e.pageX, y: e.pageY };
}

// 初始化中心位置
updateCenter();

window.onload = function __init__() {
    // 获取元素并检查存在性
    background = document.getElementById("background");
    content = document.getElementById("content");

    // 调试：检查元素是否存在
    console.log('Elements:', { background, content });

    updateCenter();
    window.addEventListener('resize', updateCenter);
};

window.onmousemove = function (event) {
    const mouseX = event.pageX;
    const mouseY = event.pageY;
    const dx = mouseX - centerX;
    const dy = mouseY - centerY;

    // 安全操作样式
    [background, content].forEach(el => {
        if (!el) {
            console.warn('元素未找到:', el);
            return;
        }
    });

    if (background) {
        background.style.transform = `translate(${-dx / 100}px, ${-dy / 100}px)`;
    }
    if (content) {
        content.style.transform = `translate(${dx / 50}px, ${dy / 50}px)`;
    }
};