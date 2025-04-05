window.onload = function __init__() {
    const body = document.body;
    setInterval(() => {
        body.setAttribute('style', 'width: ' + window.innerWidth + 'px;');
        console.log(window.innerWidth,body.offsetLeft);
    }, 1000 / 60);
}