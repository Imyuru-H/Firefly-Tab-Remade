# !/usr/bin/python
# **coding:utf-8**


__version__ = "0.1.0"


import os, time, random
os.environ["PYTHONIOENCODING"] = "utf-8"

start_time = time.time()

from flask import *

import log, tips

# init log
logs = log.Info()

# init flask app
app = Flask(__name__)
app.static_folder = "static"

BG_PATH = 'background-1.mp4'

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
    app.run(debug=True, use_reloader=False, port=8080)