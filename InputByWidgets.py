# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets


class MyMessageBox(QMessageBox):
    """
    继承QMessageBox，是为了能够重载它的closeEvent,减少它的一些不必要的功能。
    否则，点击右上角红色X后，reply将直接赋值为QMessageBox.Abort(值为262144)，
    将会直接退出主程序，而这与用户习惯严重不符"""

    def __init__(self):
        super().__init__()

    def closeEvent(self, QCloseEvent):
        pass


def my_message_box(Text, DetailedText):
    """生成错误消息对话框，其中参数Text为错误的基本描述，DetailedText为详细描述"""
    msgBox = MyMessageBox()
    msgBox.setWindowTitle('错误！')
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText(Text)
    msgBox.setStandardButtons(QMessageBox.Abort | QMessageBox.Retry)
    msgBox.setDefaultButton(QMessageBox.Retry)
    msgBox.setDetailedText(DetailedText)
    reply = msgBox.exec()
    pass

    if reply == QMessageBox.Abort:
        sys.exit(app.exec_())  # 退出时把程序清理干净
    else:
        return False


class WidgetWindow(object):
    """控件输入法窗体：一个用于对主界面进行各种处理的类，负责添加控件、增加使用逻辑等"""

    def __init__(self, MainWindow):
        """把刚开始的控件全部放到主界面上去"""

        self.elements = list()
        '记录电路元件信息'
        self.widgets = list()
        self.this_win = MainWindow
        '记住此主界面，后期添加新控件时使用'
        self.current_x = 10
        '新添加的控件的位置坐标'
        self.current_y = 100
        self.current_wgt = list()
        '新添加的控件'
        self.this_elem = [None]
        '当前输入好的电路元件'

        # 建立主窗口
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.putin_help = QtWidgets.QLabel(self.centralwidget)
        self.putin_help.setGeometry(QtCore.QRect(0, 0, 221, 21))
        self.putin_help.setObjectName("putin_help")

        font = QtGui.QFont()
        font.setPointSize(15)
        MainWindow.setFont(font)

        # 输入结点数目
        self.node_splt = QtWidgets.QSplitter(self.centralwidget)
        self.node_splt.setGeometry(QtCore.QRect(10, 30, 281, 26))
        self.node_splt.setOrientation(QtCore.Qt.Horizontal)
        self.node_splt.setObjectName("node_splt")
        self.node_help = QtWidgets.QLabel(self.node_splt)
        self.node_help.setObjectName("node_help")
        self.node_in = QtWidgets.QLineEdit(self.node_splt)
        self.node_in.setObjectName("node_in")

        # 元件输入提示
        self.elemhelp_splt = QtWidgets.QSplitter(self.centralwidget)
        self.elemhelp_splt.setGeometry(QtCore.QRect(10, 70, 371, 20))
        self.elemhelp_splt.setOrientation(QtCore.Qt.Horizontal)
        self.elemhelp_splt.setObjectName("elemhelp_splt")
        self.label_3 = QtWidgets.QLabel(self.elemhelp_splt)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.elemhelp_splt)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.elemhelp_splt)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.elemhelp_splt)
        self.label_6.setObjectName("label_6")

        # 第一个元件的普通输入控件组
        self.elemin_splt = QtWidgets.QSplitter(self.centralwidget)
        self.elemin_splt.setGeometry(QtCore.QRect(10, 100, 371, 26))
        self.elemin_splt.setOrientation(QtCore.Qt.Horizontal)
        self.elemin_splt.setObjectName("elemin_splt")
        self.classchoose_box = QtWidgets.QComboBox(self.elemin_splt)
        self.classchoose_box.setObjectName("classchoose_box")

        infomation = ['请选择元件', '电阻', '电导', '电流源', '电压源', 'CCCS', 'VCCS', 'VCVS', 'CCVS', "电容", "电感"]
        self.classchoose_box.addItems(infomation)
        self.classchoose_box.activated[str].connect(self.type_choose)

        self.value_in = QtWidgets.QLineEdit(self.elemin_splt)
        self.value_in.setObjectName("value_in")
        self.from_in = QtWidgets.QLineEdit(self.elemin_splt)
        self.from_in.setObjectName("from_in")
        self.to_in = QtWidgets.QLineEdit(self.elemin_splt)
        self.to_in.setObjectName("to_in")

        # 第一个元件的受控量节点位置输入
        self.contral_splt = QtWidgets.QSplitter(self.centralwidget)
        self.contral_splt.setGeometry(QtCore.QRect(10, 130, 371, 26))
        self.contral_splt.setOrientation(QtCore.Qt.Horizontal)
        self.contral_splt.setObjectName("contral_splt")
        self.ctrlfrom_help = QtWidgets.QLabel(self.contral_splt)
        self.ctrlfrom_help.setObjectName("ctrlfrom_help")
        self.ctrlfrom_in = QtWidgets.QLineEdit(self.contral_splt)
        self.ctrlfrom_in.setObjectName("ctrlfrom_in")
        self.ctrlto_help = QtWidgets.QLabel(self.contral_splt)
        self.ctrlto_help.setObjectName("ctrlto_help")
        self.ctrlto_in = QtWidgets.QLineEdit(self.contral_splt)
        self.ctrlto_in.setObjectName("ctrlto_in")

        # 两个按钮的控件组
        self.button_splt = QtWidgets.QSplitter(self.centralwidget)
        self.button_splt.setGeometry(QtCore.QRect(10, 160, 371, 28))
        self.button_splt.setOrientation(QtCore.Qt.Horizontal)
        self.button_splt.setObjectName("button_splt")
        self.addmore_bt = QtWidgets.QPushButton(self.button_splt)
        self.addmore_bt.setObjectName("addmore_bt")
        self.addmore_bt.clicked.connect(self.try_addmore)

        self.stopputin_bt = QtWidgets.QPushButton(self.button_splt)
        self.stopputin_bt.setObjectName("stopputin_bt")
        self.stopputin_bt.clicked.connect(self.try_stop)

        # 主窗口上下栏
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.actionhelp = QtWidgets.QAction(MainWindow)
        self.actionhelp.setObjectName("actionhelp")
        self.menu.addAction(self.actionhelp)
        self.menubar.addAction(self.menu.menuAction())

        self.current_wgt = [self.contral_splt, self.classchoose_box, self.value_in, self.from_in, self.to_in,
                            self.ctrlfrom_in, self.ctrlto_in]

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.putin_help.setText(_translate("MainWindow", "请输入电路元件：（SI）"))
        self.node_help.setText(_translate("MainWindow", "结点数："))
        self.label_3.setText(_translate("MainWindow", "元件类型："))
        self.label_4.setText(_translate("MainWindow", "值/系数："))
        self.label_5.setText(_translate("MainWindow", "from："))
        self.label_6.setText(_translate("MainWindow", "to："))
        self.ctrlfrom_help.setText(_translate("MainWindow", "ctrl_from："))
        self.ctrlto_help.setText(_translate("MainWindow", "ctrl_to："))
        self.addmore_bt.setText(_translate("MainWindow", "继续添加"))
        self.stopputin_bt.setText(_translate("MainWindow", "输入完成"))
        self.menu.setTitle(_translate("MainWindow", "帮助"))
        self.actionhelp.setText(_translate("MainWindow", "help"))

    def type_choose(self, text):
        # 选择元件类型，并删除不必要的输入框

        # infomation = ['电阻', '电导', '电流源', '电压源', 'CCCS', 'VCCS', 'VCVS', 'CCVS', "电容", "电感"]
        if text not in ['CCCS', 'VCCS', 'VCVS', 'CCVS']:
            self.current_wgt[0].hide()
            self.button_splt.move(self.current_x, self.current_y + 30)
        else:
            self.current_wgt[0].show()
            self.button_splt.move(self.current_x, self.current_y + 60)
        self.this_elem[0] = text

    def try_addmore(self):
        try:
            self.addmore()
        except ValueError as reason:
            my_message_box('数值输错了！', '详细信息：'+str(reason))
            self.this_elem = [self.this_elem[0]]

    def addmore(self):
        """读取当前元件的数据，并添加新控件"""
        self.node_num = int(self.node_in.text())
        for i in range(2, 5):
            self.this_elem.append(float(self.current_wgt[i].text()))
        if self.this_elem[0] in ['CCCS', 'VCCS', 'VCVS', 'CCVS']:
            self.this_elem.append(float(self.current_wgt[5].text()))
            self.this_elem.append(float(self.current_wgt[6].text()))
        if self.warnings():
            print('这个元件：')
            print(self.this_elem)
            self.elements.append(self.this_elem)
            self.widgets.append(self.current_wgt)
            print('全部元件：')
            print(self.elements)
            self.create_wgt()
            self.this_elem = [None]
        else:
            self.this_elem = [self.this_elem[0]]

    def create_wgt(self):
        """创建新控件"""
        if self.current_y + 70 + 60 + 30 >= self.this_win.height() - 50:
            # 假如下方越界，就换到下一列
            self.current_y = 40
            self.current_x += 400

            # 画竖线
            vertical_line = QtWidgets.QFrame(self.centralwidget)
            vertical_line.setGeometry(QtCore.QRect(self.current_x - 20, 0, 20, 1000000))
            vertical_line.setFrameShape(QtWidgets.QFrame.VLine)
            vertical_line.setFrameShadow(QtWidgets.QFrame.Sunken)
            vertical_line.setObjectName("centual_line")
            vertical_line.show()

            # 每一列都要有新的输入提示
            elemhelp_splt_2 = QtWidgets.QSplitter(self.centralwidget)
            elemhelp_splt_2.setGeometry(QtCore.QRect(self.current_x, 10, 371, 20))
            elemhelp_splt_2.setOrientation(QtCore.Qt.Horizontal)
            elemhelp_splt_2.setObjectName("elemhelp_splt_2")
            label_7 = QtWidgets.QLabel(elemhelp_splt_2)
            label_7.setObjectName("label_7")
            label_8 = QtWidgets.QLabel(elemhelp_splt_2)
            label_8.setObjectName("label_8")
            label_9 = QtWidgets.QLabel(elemhelp_splt_2)
            label_9.setObjectName("label_9")
            label_10 = QtWidgets.QLabel(elemhelp_splt_2)
            label_10.setObjectName("label_10")

            label_7.setText("元件类型：")
            label_8.setText("值/系数：")
            label_9.setText("from：")
            label_10.setText("to：")

            elemhelp_splt_2.show()
        else:
            # 没越界，就移动坐标到下一个位置
            if self.this_elem[0] in ['CCCS', 'VCCS', 'VCVS', 'CCVS']:
                self.current_y += 70
            else:
                self.current_y += 40

        # 按钮不生成新的，只移动
        self.button_splt.move(self.current_x, self.current_y + 60)
        # 新的输入控件组
        elemin_splt_2 = QtWidgets.QSplitter(self.centralwidget)
        elemin_splt_2.setGeometry(QtCore.QRect(self.current_x, self.current_y, 371, 26))
        elemin_splt_2.setOrientation(QtCore.Qt.Horizontal)
        elemin_splt_2.setObjectName("elemin_splt_2")

        infomation = ['请选择元件', '电阻', '电导', '电流源', '电压源', 'CCCS', 'VCCS', 'VCVS', 'CCVS', "电容", "电感"]
        classchoose_box_2 = QtWidgets.QComboBox(elemin_splt_2)
        classchoose_box_2.setObjectName("classchoose_box_2")
        classchoose_box_2.addItems(infomation)
        classchoose_box_2.activated[str].connect(self.type_choose)

        value_in_2 = QtWidgets.QLineEdit(elemin_splt_2)
        value_in_2.setObjectName("value_in_2")
        # value_in_2.setText('0')
        from_in_2 = QtWidgets.QLineEdit(elemin_splt_2)
        from_in_2.setObjectName("from_in_2")
        to_in_2 = QtWidgets.QLineEdit(elemin_splt_2)
        to_in_2.setObjectName("to_in_2")
        # 控制量输入控件组
        contral_splt_2 = QtWidgets.QSplitter(self.centralwidget)
        contral_splt_2.setGeometry(QtCore.QRect(self.current_x, self.current_y + 30, 371, 26))
        contral_splt_2.setOrientation(QtCore.Qt.Horizontal)
        contral_splt_2.setObjectName("contral_splt_2")
        ctrlfrom_help_2 = QtWidgets.QLabel(contral_splt_2)
        ctrlfrom_help_2.setObjectName("ctrlfrom_help_2")
        ctrlfrom_in_2 = QtWidgets.QLineEdit(contral_splt_2)
        ctrlfrom_in_2.setObjectName("ctrlfrom_in_2")
        ctrlto_help_2 = QtWidgets.QLabel(contral_splt_2)
        ctrlto_help_2.setObjectName("ctrlto_help_2")
        ctrlto_in_2 = QtWidgets.QLineEdit(contral_splt_2)
        ctrlto_in_2.setObjectName("ctrlto_in_2")

        ctrlfrom_help_2.setText("ctrl_from：")
        ctrlto_help_2.setText("ctrl_to：")

        # new_wgt = [contral_splt_2, classchoose_box_2, value_in_2, from_in_2, to_in_2,
        #            ctrlfrom_in_2, ctrlto_in_2]

        self.current_wgt = [contral_splt_2, classchoose_box_2, value_in_2, from_in_2, to_in_2,
                            ctrlfrom_in_2, ctrlto_in_2]

        elemin_splt_2.show()
        contral_splt_2.show()

        # for i, item in enumerate(new_wgt):
        #     if i != 0:
        #         item.show()

    def try_stop(self):
        try:
            self.stop()
        except ValueError as reason:
            my_message_box('数值输错了！', '详细信息：'+str(reason))
            # self.this_elem = [self.this_elem[0]]????????????????????????????????未完成

    def stop(self):
        """输入完成。把最后输入的一个元件的信息存储起来，隐藏输入界面，并打开展示界面"""
        self.node_num = int(self.node_in.text())
        for i in range(2, 5):
            self.this_elem.append(float(self.current_wgt[i].text()))
        if self.this_elem[0] in ['CCCS', 'VCCS', 'VCVS', 'CCVS']:
            self.this_elem.append(float(self.current_wgt[5].text()))
            self.this_elem.append(float(self.current_wgt[6].text()))
        print('这个元件：')
        print(self.this_elem)
        self.elements.append(self.this_elem)
        self.widgets.append(self.current_wgt)
        print('结点个数： ' + str(self.node_num))
        print('全部元件：')
        print(self.elements)
        self.this_win.hide()

    def warnings(self):
        """针对可能出现的数值错误、输入错误等进行报错"""
        if self.node_num < 2:
            return my_message_box("总结点数目过少！", '详细信息：电路中，总结点数目应大于1.')
        # elif self.node_num not in range(0, self.node_num)

        if self.this_elem[0] in [None, '请选择元件']:
            return my_message_box("未选择元件类型！", '详细信息：电路中，每个元件都有其类型和特性。')

        if (self.this_elem[1] < 0) and (self.this_elem[0] in ['电阻', '电导', "电容", "电感"]):
            # return self.my_message_box(,)
            return my_message_box("此类元件的值不能为负数！", '详细信息：在本程序中，电阻、电导、电容、电感不能取负值。')

        if self.this_elem[2] not in range(0, self.node_num) or self.this_elem[3] not in range(0, self.node_num):
            return my_message_box('元件所在结点数取值有误！', '元件所在结点应该为正整数，且在[0,n)中，其中n为总结点数。')

        if self.this_elem[4] not in range(0, self.node_num) or self.this_elem[5] not in range(0, self.node_num):
            return my_message_box('元件控制量所在结点数取值有误！', '元件控制量所在结点应该为正整数，且在[0,n)中，其中n为总结点数。')
        return True


if __name__ == '__main__':
    # 显示输入GUI
    import cgitb  # 报错用
    import sys  # 系统

    # import threading
    cgitb.enable()  # 用于GUI程序的调试
    app = QtWidgets.QApplication(sys.argv)  # 收集命令行的参数，为运行做准备

    MainWindow = QtWidgets.QMainWindow()  # 它是程序所显示的主界面
    ui = WidgetWindow(MainWindow)  # 实例化对象
    MainWindow.show()  # 在屏幕上显示

    sys.exit(app.exec_())  # 退出时把程序清理干净
