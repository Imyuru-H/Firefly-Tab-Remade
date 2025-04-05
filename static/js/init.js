const body = document.body;

(function () {
    setInterval(() => {
        const body_left = body.offsetLeft;
        body.style.width = window.innerWidth;
        console.log(window.innerWidth);
    }, 1000 / 60);
})();