# coding = utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from uis.ui_webchatmain import Ui_Form


class WidChatMain(QWidget):  # 窗体

    def __init__(self, chat_):
        super().__init__()
        # self.setGeometry(100, 100, 800, 600)
        # self.setWindowTitle('聊天')
        self.chat = chat_
        self.ui_main = Ui_Form()
        self.ui_main.setupUi(self)

        # 处理chat收到信息的信号
        self.chat.sign_coming_msg.connect(self.show_msg)

        # 添加模式，和列表框绑在一起
        self.model = QStandardItemModel()
        self.ui_main.listView.setModel(self.model)

        # 列表框绑定信号处理，(点击的对象)传递给函数index
        self.ui_main.listView.clicked.connect(self.select_user)
        # 发送按钮绑定信号处理，发送信息
        self.ui_main.pushButton.clicked.connect(self.send_msg)

    def show_user_list(self):
        # 从helper中获取用户列表
        lst_users = self.chat.get_friends()
        # 显示列表到列表框
        for user_ in lst_users:
            user_name = user_['UserName']  # 用户id
            nick_name = user_['NickName']  # 用户昵称
            icon_head = QIcon('imgs/user.jpg')  # 自己头像，图片路径
            item_ = QStandardItem(icon_head, nick_name)  # 形成模式中的数据项
            item_.setData(user_name)  # 用户id也放在模式中，但是隐式存放，item_中显示只有图标和昵称
            self.model.appendRow(item_)  # 添加到模式中

    def select_user(self, index):
        # 返回选择的行号
        row = index.row()
        # index.data()  # 用户昵称
        # self.model.item(row).data()  # 模型中隐式的数据(用户id)，通过行号来找到对应用户的id
        self.current_user = self.model.item(row).data()

    def send_msg(self):
        # 获取文本信息
        msg = self.ui_main.lineEdit.text()
        # 发送，使用helper
        self.chat.send_msg(self.current_user, msg)

    def show_msg(self, msg):
        self.setWindowTitle(msg)  # 收到信息显示在标题上