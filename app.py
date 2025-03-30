# !/usr/bin/python
# **coding:utf-8**


__version__ = "re-0.0.1"


import os, sys, time, random
os.environ["PYTHONIOENCODING"] = "utf-8"

start_time = time.time()

from flask import *
import logging
import queue
import threading
from PyQt5.QtWidgets import QApplication

import tips

# 配置应用设置
CONFIGS = {
    'ui_logging' : True,
    'flask_debug' : False,
    'flask_port' : 8080,
    'app_name' : 'Firefly',
    'bg_path' : 'background-1.mp4',
}

if CONFIGS['ui_logging']:
    import UiLog as log
else:
    import NonUiLog as log

# init log
app_qt = QApplication([])
logs = log.LoggerApp()

# init flask app
app = Flask(CONFIGS['app_name'])
app.static_folder = "static"

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
        "background" : f"/static/background/{CONFIGS['bg_path']}"
    }

    return render_template('firefly.html', **kwargs), logs.info("return firefly.html.")


if __name__ == "__main__":
    end_time = time.time()
    logs.info(f"App start duration: {end_time-start_time:.2f}s")
    
    def run_flask_app():
        app.run(debug=CONFIGS['flask_debug'], use_reloader=False, port=CONFIGS['flask_port'])
    
    # 启动 Flask 应用的后台线程
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    logs.info(f" * Serving Flask app '{CONFIGS['app_name']}' on port {CONFIGS['flask_port']}",
              f" * Debug mode: {'on' if CONFIGS['flask_debug'] else 'off'}",)
    
    # 显示日志窗口并启动 Qt 事件循环
    logs.show()
    sys.exit(app_qt.exec_())