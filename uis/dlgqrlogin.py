# coding = utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from uis.ui_login import Ui_ui_login


class DlgQRLogin(QDialog):
    """
    二维码登录对话框
    """

    def __init__(self, chat_):
        super().__init__()
        # self.setGeometry(100, 100, 400, 300)  # 加密锤
        # self.setWindowTitle('登录')
        self.chat = chat_
        self.ui = Ui_ui_login()
        self.ui.setupUi(self)

        # 接收二维码
        self.chat.sign_qr.connect(self.show_qr)  # qr信号绑定在一个糟函数上

    def show_qr(self, qrcode):
        img_qr = QImage.fromData(qrcode)  # 转成图片
        pix_qr = QPixmap.fromImage(img_qr)  # 图片转换成像素
        self.ui.lbl_qr.setPixmap(pix_qr)  # 把像素加载到标签框
        self.ui.lbl_qr.setScaledContents(True)  # 设置二维码按窗体大小铺
