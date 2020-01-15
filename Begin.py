# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class begin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('开始程序')
        self.show()


if __name__ == '__main__':
    import cgitb    # 报错用
    import sys  # 系统
    cgitb.enable()  # 用于GUI程序的调试
    app = QtWidgets.QApplication(sys.argv)  # 收集命令行的参数，为运行做准备

    b=begin()

    sys.exit(app.exec_())   # 退出时把程序清理干净
