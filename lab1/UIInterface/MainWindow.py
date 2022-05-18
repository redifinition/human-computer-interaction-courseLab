# 1853572 梁乔
import logging
import sys
from os.path import exists
import clock_style
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QMovie
from PyQt5.QtWidgets import *
from pyqt5_plugins.examplebutton import QtWidgets
from ASRModel.CommandExecutor import CommandExecutorSingleton, CommandExecutor
from ASRModel.WorkerThread import InputWorker


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Joe ASR World')
        self.set_bg('montery.jpg')
        self.resize(960,690)
        self.setMinimumWidth(660)
        self.setMinimumHeight(690)
        self.set_up_ui()

    def set_up_ui(self):

        # 全局布局
        wwg = QWidget(self)

        #交互框放置于网格布局
        # 创建网格布局空间
        gl = QGridLayout(wwg)
        self.setLayout(gl)
        # 标题框
        titleCard = QLabel('',self)
        titleCard.setStyleSheet('mim-height:200px;background-color: rgb(0,0,0,0.3);border-radius:40px')
        gl.addWidget(titleCard,0,0,1,3)
        # 交互结果框
        dialog = QLabel('',self)
        #dialog.resize(400,400)
        dialog.setStyleSheet("background-color: rgb(0,0,0,0.3);border-radius:40px;border-width:10px")
        dialog.setFrameShape(QtWidgets.QFrame.Box)
        gl.addWidget(dialog,1,0,1,3)

        gl.setRowStretch(0,1)
        gl.setRowStretch(1,4)
        #
        # # 框架内的内容
        # titleLayout = QGridLayout()
        # titleCard.setLayout(titleLayout)
        # robotAvatar = QLabel('dwwd')
        # titleLayout.addWidget(robotAvatar,0,0)
        # space = QLabel('')
        # titleLayout.addWidget(space,0,1)
        # 创建布局

        #1.创建顶部菜单布局
        header_layout = QBoxLayout(QBoxLayout.LeftToRight)
        # 把布局管理器对象设置给需要布局的父控件
        titleCard.setLayout(header_layout)
        # 添加需要布局的控件
        #1.1 创建一个ASR头像

        siriAvatar = QLabel('',self)
        siriAvatar.resize(100,100)
        siriAvatar.setStyleSheet('max-width:100px;max-height:100px;min-width:100px;min-height:100px;border-radius:50px;background-color: none;border-width:0px')
        png = QPixmap('siri.png')
        siriAvatar.setPixmap(png)
        siriAvatar.setScaledContents(True)
        #1.2 创建欢迎语句
        welcomeContent = QLabel('''<font color=black face='Consolas' size=5 >Welcome to Joe's ASR World!!!<font>''')
        welcomeContent.setStyleSheet('border-radius:20px;min-width:500px;max-height:80px;background-color: rgb(100,100,100,0.3);border-width:0px')
        welcomeContent.resize(1000,80)
        header_layout.addWidget(siriAvatar)
        header_layout.addWidget(welcomeContent)
        header_layout.addSpacing(500)
        header_layout.setSpacing(10)

        # 创建主题布局
        content_layout = QBoxLayout(QBoxLayout.TopToBottom);

        # 显示时间的水平布局
        clock_layout = QBoxLayout(QBoxLayout.LeftToRight);
        self.clock_hh = QLabel()
        self.clock_hh.setAlignment(Qt.AlignCenter)
        self.clock_hh.setObjectName('labelHour')
        self.clock_hh.setStyleSheet(clock_style.style)
        self.clock_mm = QLabel()
        self.clock_mm.setAlignment(Qt.AlignCenter)
        self.clock_mm.setObjectName('labelMinute')
        self.clock_mm.setStyleSheet(clock_style.style)
        self.clock_ss = QLabel()
        self.clock_ss.setAlignment(Qt.AlignCenter)
        self.clock_ss.setObjectName('labelSecond')
        self.clock_ss.setStyleSheet(clock_style.style)
        self.point_1 = QLabel(":")
        self.point_1.setObjectName("labelEmty")
        self.point_1.setAlignment(Qt.AlignCenter)
        self.point_1.setStyleSheet(clock_style.style)
        self.point_2 = QLabel(":")
        self.point_2.setAlignment(Qt.AlignCenter)
        self.point_2.setObjectName("labelEmty")
        self.point_2.setStyleSheet(clock_style.style)
        self.type = QLabel()
        self.type.setAlignment(Qt.AlignCenter)
        self.type.setObjectName("labelEmty")
        self.type.setStyleSheet(clock_style.style)
        clock_layout.addWidget(self.clock_hh)
        clock_layout.addWidget(self.point_1)
        clock_layout.addWidget(self.clock_mm)
        clock_layout.addWidget(self.point_2)
        clock_layout.addWidget(self.clock_ss)
        clock_layout.addWidget(self.type)
        clock_layout.addStretch(100)
        #添加布局
        content_layout.addLayout(clock_layout)
        dialog.setLayout(content_layout)

        # 使用Timer 记录时间
        clock_timer = QTimer(self)
        clock_timer.timeout.connect(self.displayTime)
        clock_timer.start(1000)

        self.main_text = QLabel('Hello bro!What can I help you? Say \'Hey bro \' to get more help.')
        self.main_text.setStyleSheet(clock_style.style)
        self.main_text.setWordWrap(True)
        content_layout.addWidget(self.main_text)
        content_layout.addStretch(100)

        middle_layout = QBoxLayout(QBoxLayout.LeftToRight)

        # 添加loading
        self.loading = QLabel('')
        movie = QMovie('load1.gif')
        self.loading.setMovie(movie)
        movie.start()
        self.loading.setStyleSheet(clock_style.style)
        content_layout.addWidget(self.loading)
        self.loading.setVisible(False)
        self.said_text = QLabel('')
        self.said_text.setStyleSheet(clock_style.style)
        self.main_text.setWordWrap(True)
        middle_layout.addWidget(self.said_text)

        content_layout.addLayout(middle_layout)


        # 添加底部说话按钮
        self.say_button = QLabel('')
        self.say_button.resize(100, 100)
        self.say_button.setStyleSheet(
            'QLabel{cursor:pointer;max-width:100px;max-height:100px;min-width:100px;min-height:100px;border-radius:50px;background-color: none;border-width:0px}')
        png = QPixmap('microphone.png')
        self.say_button.setPixmap(png)
        self.say_button.setScaledContents(True)
        self.say_button.mousePressEvent = self.link_hovered
        # 设置麦克风按钮的鼠标交互
        gl.addWidget(self.say_button,2,1,1,1)


    def link_hovered(self,test):

        # 改变交互窗口的指令
        self.main_text.setText('I am hearing...')
        self.thread = InputWorker()
        self.loading.setVisible(True)
        self.thread.start()
        self.thread.sig.connect(self.show_result)

    def show_result(self,str):
        self.loading.setVisible(False)
        self.main_text.setText(self.thread.command_executor.getResponse(str))
        self.said_text.setText('You just have said:'+ self.thread.command_executor.said_text)


    def set_bg(self, image):
        """设置本地背景图片

        形参 image 可以是 QPixmap 实例、资源路径或磁盘路径。
        """
        if type(image) == QPixmap:
            self._bgimg = image
        elif type(image) == str:
            image = image.strip()
            if image[:4] == 'http':
                logging.warning("set_bg(self, image: Union[QPixmap, path])" +
                                "\n:  The argument 1 is a URL like, you might want to use" +
                                " set_web_bg(self, url, params=None, **kwargs).")
                self.set_web_bg(image)
                return None
            elif not image:
                logging.warning("set_bg(self, image: Union[QPixmap, path])" +
                                "\n:  The argument 1 is null.")
                return None
            elif not exists(image) and image[:2] != ':/':
                logging.warning("set_bg(self, image: Union[QPixmap, path])" +
                                "\n:  The file '{}' is inexistence.".format(image))
                return None
            image = QPixmap(image)
            self._bgimg = image
        else:
            return None
        adapt_image = self._adapt_bg(self._bgimg)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(adapt_image))
        self.setPalette(palette)

    def _adapt_bg(self, image):
        """返回适应窗口大小的背景图片"""
        image = image.scaled(self.width(), self.height(), \
                             Qt.KeepAspectRatioByExpanding, \
                             Qt.SmoothTransformation)
        return image

    def resizeEvent(self, event):
        """重写窗口大小改变事件，实现自适应背景图片"""

        if not self._bgimg:
            return None
        palette = QPalette()
        img = self._adapt_bg(self._bgimg)
        palette.setBrush(QPalette.Window, QBrush(img))
        self.setPalette(palette)

    # 显示时间函数
    def displayTime(self):
        currentTime = QTime.currentTime()
        hours = currentTime.toString('hh')
        minutes = currentTime.toString('mm')
        seconds = currentTime.toString('ss')
        meridiem = currentTime.toString('ap')
        self.type.setText(meridiem.upper())
        self.clock_hh.setText(hours)
        self.clock_mm.setText(minutes)
        self.clock_ss.setText(seconds)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())



