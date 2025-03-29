# !/usr/bin/python
# **coding:utf-8**


__version__ = '0.3.0'

"""
+------------------+------------+
| Author           : Imyuru_    |
| Version          : 0.3.0      |
| Last update time : 2025-3-29  |
+------------------+------------+

Update Features:
 - rebuild the app with PyQt5 from tkinter.
"""


import os, sys
import threading
os.environ["PYTHONIOENCODING"] = "utf-8"

import PyQt5
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QVBoxLayout, QHBoxLayout, QLabel, 
                             QTextEdit, QTableWidget, QTableWidgetItem, 
                             QHeaderView)
from PyQt5.QtGui import QColor, QTextCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QMutex

import platform, psutil, cpuinfo, GPUtil
from prettytable import PrettyTable
from datetime import datetime


CONFIG = {
    'app_name' : 'LoggerApp',
    'window_size' : (1280, 720),
    'font_family' : 'Consolas',
    'font_size' : 10
}

DARK_THEME = {
    'background' : '#191919',
}


class LogConsumer(QThread):
    log_received = pyqtSignal(str, str)  # (log_type, message)
    stats_updated = pyqtSignal(dict)     # counters dict

    def __init__(self):
        super().__init__()
        self.running = True
        self.mutex = QMutex()
        self.log_queue = []
        self.counters = {
            'info': 0,
            'error': 0,
            'false': 0,
            'debug': 0
        }
    
    def push_log(self, log_type, message):
        self.mutex.lock()
        self.log_queue.append((log_type, message))
        self.mutex.unlock()

    def run(self):
        while self.running:
            self.mutex.lock()
            if self.log_queue:
                log_type, message = self.log_queue.pop(0)
                self.counters[log_type] += 1
                self.log_received.emit(log_type, message)
                self.stats_updated.emit(self.counters.copy())
            self.mutex.unlock()
            self.msleep(1)

    def stop(self):
        self.running = False
        self.wait()

class LoggerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self._init_ui()
        self._init_worker()
        self.info("System Info:", *self.get_sys_info())
    
    def _init_ui(self):
        self.setWindowTitle(CONFIG['app_name'])
        self.setGeometry(100, 100, *CONFIG['window_size'])
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1A1A1A;
            }
            QTextEdit {
                background-color: #2D2D2D;
                color: #D4D4D4;
                border: none;
            }
            QLabel {
                color: #D4D4D4;
            }
            QHeaderView::section {
                background-color: #3C3C3C;
                color: #D4D4D4;
            }
        """)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
         # Log display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text)

        # Stats panel
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        self.stats_labels = {
            'info': QLabel("INFO: 0"),
            'error': QLabel("ERROR: 0"),
            'false': QLabel("FALSE: 0"),
            'debug': QLabel("DEBUG: 0")
        }
        for label in self.stats_labels.values():
            # label.setStyleSheet("font-weight: bold;")
            stats_layout.addWidget(label)
        
        main_layout.addWidget(stats_widget)

    def _init_worker(self):
        self.consumer = LogConsumer()
        self.consumer.log_received.connect(self.append_log)
        self.consumer.stats_updated.connect(self.update_stats)
        self.consumer.start()

    def get_sys_info(self):
        info = {
            "OS Info" : f"{platform.system()} {platform.release()}",
            "Python Version" : platform.python_version(),
            "CPU" : f"{cpuinfo.get_cpu_info()['brand_raw']} ×{psutil.cpu_count(logical=False)} ",
            "RAM" : f"{psutil.virtual_memory().total//(1024**3):.2f} GB"
        }
        try:
            gpus = GPUtil.getGPUs()
            for i, gpu in enumerate(gpus):
                info[f"GPU {i}"] = f"{gpu.name}"
                info[f"VRAM {i}"] = f"{gpu.memoryTotal} MB"
        except:
            info["GPU"] = "Not Available"
        
        table = PrettyTable(['1','2'])
        for kwargs in info.items():
            table.add_row([*kwargs])

        table = str(table).split("\n")

        for i in range(len(table)):
            table[i] = table[i].replace(" ","&nbsp;")

        return table
    
    @pyqtSlot(str, str)
    def append_log(self, log_type:str, message:str):
        color_map = {
            'info' : '#C0C000',
            'error' : '#C03030',
            'false' : '#C00000',
            'debug' : '#C000C0',
            'timestamp' : '#858585',
            'content' : '#D4D4D4'
        }
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        log_label = f"[{log_type.upper()}]&nbsp;" if log_type == "info" else f"[{log_type.upper()}]"

        log_html = f"""
            <div style="margin-bottom: 2px;
                        line-height: 1.4em;
                        font-family: {CONFIG['font_family']};
                        font-size: {CONFIG['font_size']}pt;
                        border-bottom: 1px solid #101010;
                        padding: 1px 0;">
                <span style="color: {color_map['timestamp']}">{timestamp}</span>
                <span style="color: {color_map[log_type]}">{log_label}</span>
                <span style="color: {color_map['content']}">{message}</span>
            </div>
        """
        self.log_text.moveCursor(QTextCursor.End)
        self.log_text.insertHtml(log_html)
        self.log_text.insertPlainText("\n")
        self.log_text.ensureCursorVisible()
    
    @pyqtSlot(dict)
    def update_stats(self, counters:dict):
        for log_type, count in counters.items():
            self.stats_labels[log_type].setText(
                f"{log_type.upper()}: {count}"
            )
    
    def closeEvent(self, event):
        if hasattr(self, 'consumer'):  # 安全检查
            self.consumer.stop()
        return super().closeEvent(event)
    
    # Public API methods
    def info(self, *messages):
        for message in messages:
            self.consumer.push_log('info', message)
    
    def error(self, *messages):
        for message in messages:
            self.consumer.push_log('error', message)

    def false(self, *messages):
        for message in messages:
            self.consumer.push_log('false', message)

    def debug(self, *messages):
        for message in messages:
            self.consumer.push_log('debug', message)