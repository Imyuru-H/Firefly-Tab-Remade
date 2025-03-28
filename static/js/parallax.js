function updateCenter() {
    // 计算当前页面的中心点
    globalThis.centerX = document.body.offsetWidth / 2;
    globalThis.centerY = document.body.offsetHeight / 2;
}

function getMousePos(event) {
    var e = event || window.event;
    return { "x": e.screenX, "y": e.screenY };
}

(function (){
    updateCenter();
})();

window.onload = function __init__() {
    globalThis.background = document.getElementById("background");
    globalThis.content = document.getElementById("content");
    globalThis.particle = document.getElementById("particle");
    // 初始化并更新页面中心坐标
    updateCenter();
    // 监听窗口大小变化以更新中心坐标
    window.addEventListener('resize', updateCenter);
};

window.onmousemove = function(event) {
    // 获取当前鼠标位置（基于文档坐标）
    const mouseX = event.pageX - document.body.offsetWidth / 2;
    const mouseY = event.pageY;
    
    // 计算与中心点的偏移量
    const dx = mouseX - centerX;
    const dy = mouseY - centerY;
    
    // 应用视差效果
    background.style.transform = `translate(${-dx/100}px, ${-dy/100}px)`;
    particle.style.transform = `translate(${-dx/100}px, ${-dy/100}px)`;
    content.style.transform = `translate(${dx/50}px, ${dy/50}px)`;
};