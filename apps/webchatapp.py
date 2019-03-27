# coding = utf-8
"""
作用：组合界面，业务封装，形成独立的应用逻辑
"""
from PyQt5.QtCore import *

from uis.dlgqrlogin import DlgQRLogin
from uis.widchatmain import WidChatMain
from helpers.webchathelper import WebChatHelper


class WebChatApp(QObject):
    """
    负责组合登录界面，聊天界面，微信访问模块，形成微信聊天的功能
    """

    def __init__(self):
        super().__init__()

        # 调用辅助类实现登录
        self.chat = WebChatHelper()

        self.ui_login = DlgQRLogin(self.chat)  # 构建登录对象
        self.ui_login.show()  # 显示登录对象
        self.ui_main = WidChatMain(self.chat)  # 构建聊天窗体对象
        self.chat.sign_login_ok.connect(self.show_chat_main)
        self.chat.start()  # start是开始线程排队，挨个run每个线程

    def show_chat_main(self):
        # 隐藏登录
        self.ui_login.hide()
        # 释放登录
        self.ui_login.destroy()
        # 加载用户列表
        self.ui_main.show_user_list()
        # 显示聊天窗体
        self.ui_main.show()