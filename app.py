# !/usr/bin/python
# **coding:utf-8**


__version__ = "re-0.0.1"


import os, time, random
os.environ["PYTHONIOENCODING"] = "utf-8"

start_time = time.time()

from flask import *
import logging
import queue
import threading

import log, tips

# init log
logs = log.LoggerApp()
# 在单独的线程中启动 Tkinter 主循环
tk_thread = threading.Thread(target=logs.start, daemon=True)
tk_thread.start()

# init flask app
app = Flask(__name__)
app.static_folder = "static"

BG_PATH = 'background-1.mp4'

# 配置 Flask 日志处理器
app.logger.handlers = []

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.handlers = []  # 清空所有处理器
werkzeug_logger.propagate = False  # 禁止向上传播日志
werkzeug_logger.setLevel(logging.CRITICAL)  # 设置日志级别

log_queue = queue.Queue(-1) # 无限制队列

@app.after_request
def capture_response_data(response):
    # 获取请求路径、方法、状态码、响应时间等信息
    data = {
        "method": request.method,
        "path": request.path,
        "status_code": response.status_code,
        "client_ip": request.remote_addr,
        "user_agent": str(request.user_agent)
    }
    log_content = f"- {data['method']} {data['status_code']} - from {data['client_ip']}, calling {data['path']}"

    if data["status_code"]//100 == 2 or data["status_code"]//100 == 3:
        logs.info(log_content)
    elif data["status_code"]//100 == 4:
        logs.error(log_content)
    elif data["status_code"]//100 == 5:
        logs.false(log_content)
    
    return response

@app.route('/')
def index():
    kwargs = {
        "tip" : random.choice(tips.tips),
        "background" : f"/static/background/{BG_PATH}"
    }

    return render_template('firefly.html', **kwargs), logs.info("return firefly.html.")


if __name__ == "__main__":
    end_time = time.time()
    logs.info(f"App start duration: {end_time-start_time:.2f}s")
    
    # 启动web app
    app.run(debug=False, use_reloader=False, port=8080)