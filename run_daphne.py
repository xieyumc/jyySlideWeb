import os
import threading
import webbrowser
from daphne.cli import CommandLineInterface

def open_browser():
    import time
    # 等待服务器启动
    time.sleep(5)
    # 打开浏览器访问指定的 URL
    webbrowser.open('http://localhost:10001')

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jyy_slide_web.settings')

    # 启动线程来打开浏览器
    threading.Thread(target=open_browser).start()

    # 运行 Daphne 服务器
    CommandLineInterface().run(['-b', '0.0.0.0', '-p', '10001', 'jyy_slide_web.asgi:application'])