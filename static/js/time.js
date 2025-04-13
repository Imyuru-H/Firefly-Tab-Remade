(function () {
    let hourElmt, minuteElmt, secondElmt;
    let lastSecond = -1;

    function padZero(num) {
        return num.toString().padStart(2, '0');
    }

    function updateTime() {
        const now = new Date();
        const currentSecond = now.getSeconds();

        // 只有秒数变化时更新DOM
        if (currentSecond !== lastSecond) {
            hourElmt.textContent = padZero(now.getHours());
            minuteElmt.textContent = padZero(now.getMinutes());
            secondElmt.textContent = padZero(currentSecond);
            lastSecond = currentSecond;
        }

        requestAnimationFrame(updateTime);
    }

    function initTime() {
        hourElmt = document.getElementById('hours');
        minuteElmt = document.getElementById('minutes');
        secondElmt = document.getElementById('seconds');

        // 立即显示初始时间
        updateTime();
    }

    window.addEventListener('load', initTime);

    window.onbeforeunload = function () {
        cancelAnimationFrame(updateTime);
    };
})();