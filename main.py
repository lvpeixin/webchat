# coding = utf-8
"""
作者：
作用：启动应用，构造环境
"""

from PyQt5.QtWidgets import QApplication
import sys

from apps.webchatapp import WebChatApp


web_app = QApplication(sys.argv)

chat_app = WebChatApp()

sys.exit(web_app.exec())
