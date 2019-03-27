# coding = utf-8
from PyQt5.QtCore import *
import itchat


class WebChatHelper(QThread):
    """
    1.使用Qt多线程类，切换login和widchat；
    2.覆盖run函数，实现并发的功能；
    """

    sign_qr = pyqtSignal(bytes)  # 定义一个信号，用于二维码生成后，传递字节流二维码
    sign_login_ok = pyqtSignal()  #定义一个信号，用于登陆成功信号
    sign_coming_msg = pyqtSignal(str)  # 定义一个信号，用于传递收到的文本信息信号

    def __init__(self):
        super().__init__()

    def run(self):
        print('开始登录')

        # itchat.content 中有很多类型，这里使用TEXT文本类型，python -m pydoc itchat.content查看
        # 文本信息传递给recv_msg函数第一个参数msg
        # 这种嵌套函数，适合静态函数(往内层函数传递参数)，且内层函数又使用外部成员变量
        @itchat.msg_register(msgType=itchat.content.TEXT, isFriendChat=True, isGroupChat=True)
        def recv_msg(msg):  # 嵌套函数，既是成员变量
            if msg['MsgType'] == 1:
                self.sign_coming_msg.emit(msg['Content'])

        # 使用itchat的login方法
        itchat.login(qrCallback=self.qr_callback, loginCallback=self.login_callback)
        itchat.run()

    # (uuid, status, qrcode)->qrCallback，二维码生成后回调，状态码status=0/200正常
    def qr_callback(self, uuid, status, qrcode):
        # print('得到二维码')
        self.sign_qr.emit(qrcode)  # 发送字节流二维码

    def login_callback(self):
        print('登录成功')
        self.sign_login_ok.emit()  # 发送一个信号

    # 获取用户列表
    def get_friends(self):
        # 获取用户列表,返回列表套字典(列表0是自己)
        lst_user = []
        friends = itchat.get_friends()  # 获取好友列表
        # friends = itchat.get_chatrooms()  # 获取聊天室的用户列表
        # 每次生成的用户列表，取每个用户的昵称和序号添加到新列表
        for friend_ in friends:
            user = {}
            user['NickName'] = friend_['NickName']
            user['UserName'] = friend_['UserName']
            lst_user.append(user)
        return lst_user

    def send_msg(self, user_, msg_):  # 谁发给谁，什么信息
        itchat.send_msg(msg=msg_, toUserName=user_)


