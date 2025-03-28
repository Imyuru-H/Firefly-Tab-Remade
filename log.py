#!/usr/bin/python
# **coding:utf-8**

__version__ = 'v1.2'

"""
+------------------+-----------+
| Author           : Imyuru_   |
| Version          : v1.2      |
| Last update time : 2025-3-29 |
+------------------+-----------+
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import datetime
import platform
import psutil
import cpuinfo
import GPUtil
import threading
import queue

class LoggerApp:
    def __init__(self):
        # 初始化主线程标记
        self._main_thread = threading.get_ident()
        
        # 样式配置
        self.font_size = 10
        self.line_height = int(self.font_size * 1.4)
        self.colors = {
            'bg': '#1A1A1A',
            'text_bg': '#2D2D2D',
            'fg': '#D4D4D4',
            'time': '#858585',
            'info': '#4EC9B0',
            'error': '#D16969',
            'false': '#CE9178',
            'debug': '#B5CEA8',
            'border': '#3C3C3C'
        }

        # 初始化主窗口
        self.root = tk.Tk()
        self.root.title("Dark Logger Pro v1.2")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.colors['bg'])
        
        # 配置异步日志系统
        self.log_queue = queue.Queue()
        self.log_counters = {'info':0, 'error':0, 'false':0, 'debug':0}
        self.stat_vars = {
            'info': tk.StringVar(value="0"),
            'error': tk.StringVar(value="0"),
            'false': tk.StringVar(value="0"),
            'debug': tk.StringVar(value="0")
        }
        self._init_log_consumer()
        
        # 构建UI
        self._create_widgets()
        self._setup_style()
        self.root.protocol("WM_DELETE_WINDOW", self._safe_shutdown)

    def start(self):
        """启动 Tkinter 主循环"""
        self.root.mainloop()

    def _init_log_consumer(self):
        """启动日志消费线程"""
        self.consumer_running = True
        self.consumer_thread = threading.Thread(
            target=self._process_log_queue,
            daemon=True
        )
        self.consumer_thread.start()

    def _process_log_queue(self):
        """处理日志队列（消费者线程）"""
        while self.consumer_running or not self.log_queue.empty():
            try:
                log_type, message = self.log_queue.get(timeout=0.1)
                self.log_counters[log_type] += 1
                
                # 使用线程安全方式更新UI
                self.root.after(0, self._update_stats)
                self.root.after(0, lambda lt=log_type, msg=message: self._update_ui(lt, msg))
            except queue.Empty:
                continue

    def _create_widgets(self):
        """创建界面组件"""
        # 系统信息面板
        sys_frame = ttk.LabelFrame(self.root, text="System Information")
        sys_frame.pack(fill=tk.X, padx=15, pady=10)
        
        sys_text = tk.Text(
            sys_frame,
            height=6,
            wrap=tk.NONE,
            bg=self.colors['text_bg'],
            fg=self.colors['fg'],
            font=('Consolas', 9),
            relief=tk.FLAT
        )
        sys_text.insert(tk.END, self._get_system_info())
        sys_text.configure(state='disabled')
        sys_text.pack(fill=tk.X, padx=5, pady=5)

        # 日志显示区
        log_frame = ttk.LabelFrame(self.root, text="Log Messages")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            font=('Consolas', self.font_size),
            spacing3=self.line_height - self.font_size,
            bg=self.colors['text_bg'],
            fg=self.colors['fg'],
            insertbackground=self.colors['fg'],
            relief=tk.FLAT
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self._configure_text_tags()

        # 统计面板
        stats_frame = ttk.Frame(self.root)
        stats_frame.pack(fill=tk.X, padx=15, pady=10)
        
        stats = [
            ('INFO', 'info'), 
            ('ERROR', 'error'),
            ('FALSE', 'false'), 
            ('DEBUG', 'debug')
        ]
        for idx, (label, key) in enumerate(stats):
            ttk.Label(stats_frame, text=f"{label}:", 
                     style='Stats.TLabel').grid(
                         row=0, column=idx*2, padx=15)
            ttk.Label(stats_frame, 
                     textvariable=self.stat_vars[key],
                     style='Stats.TLabel', 
                     width=7).grid(
                         row=0, column=idx*2+1, sticky='w')

    def _setup_style(self):
        """配置TTk样式"""
        style = ttk.Style()
        style.theme_use('alt')
        
        # 框架样式
        style.configure(
            'TLabelframe',
            background=self.colors['bg'],
            foreground=self.colors['fg'],
            bordercolor=self.colors['border']
        )
        style.configure(
            'TLabelframe.Label',
            background=self.colors['bg'],
            foreground=self.colors['fg']
        )
        
        # 统计标签样式
        style.configure(
            'Stats.TLabel',
            font=('Segoe UI', 9, 'bold'),
            foreground=self.colors['fg'],
            background=self.colors['bg']
        )

    def _configure_text_tags(self):
        """配置文本颜色标签"""
        self.log_text.tag_configure(
            'time', 
            foreground=self.colors['time']
        )
        type_tags = {
            'info': self.colors['info'],
            'error': self.colors['error'],
            'false': self.colors['false'],
            'debug': self.colors['debug']
        }
        for tag, color in type_tags.items():
            self.log_text.tag_configure(
                tag, 
                foreground=color,
                font=('Consolas', self.font_size, 'bold')
            )

    def _update_ui(self, log_type: str, message: str):
        """更新日志显示（主线程安全）"""
        if threading.get_ident() != self._main_thread:
            return
        
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        log_label = f" [{log_type.upper()}]"
        space = "  " if log_type == 'info' else " "
        
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, timestamp, 'time')
        self.log_text.insert(tk.END, log_label, log_type)
        self.log_text.insert(tk.END, f"{space}{message}\n")
        self.log_text.configure(state='disabled')
        self.log_text.see(tk.END)

    def _update_stats(self):
        """更新统计显示（主线程安全）"""
        if threading.get_ident() != self._main_thread:
            return
            
        for key in self.stat_vars:
            self.stat_vars[key].set(str(self.log_counters[key]))

    def _get_system_info(self) -> str:
        """获取系统信息"""
        info = [
            f"OS\t: {platform.system()} {platform.release()}",
            f"CPU\t: {cpuinfo.get_cpu_info()['brand_raw']}",
            f"Cores\t: {psutil.cpu_count(logical=False)} Physical",
            f"RAM\t: {psutil.virtual_memory().total//(1024**3):,} GB"
        ]
        try:
            gpus = GPUtil.getGPUs()
            for i, gpu in enumerate(gpus):
                info.append(f"GPU {i+1}\t: {gpu.name} ({gpu.memoryTotal}MB)")
        except:
            info.append("GPU\t: Not Available")
        return '\n'.join(info)

    def _safe_shutdown(self):
        """安全关闭应用"""
        self.consumer_running = False
        if self.consumer_thread.is_alive():
            self.consumer_thread.join()
        self.root.destroy()

    # 公共接口方法
    def info(self, message: str):
        self.log_queue.put(('info', message))

    def error(self, message: str):
        self.log_queue.put(('error', message))

    def false(self, message: str):
        self.log_queue.put(('false', message))

    def debug(self, message: str):
        self.log_queue.put(('debug', message))

if __name__ == "__main__":
    app = LoggerApp()
    app.start()