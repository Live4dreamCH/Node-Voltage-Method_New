# -*- coding: utf-8 -*-
# from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
import sys  # 系统
# from Calculate import cal
from InputByWidgets import WidgetWindow

if __name__ == '__main__':
    # 显示输入GUI
    import cgitb  # 报错用
    cgitb.enable()  # 用于GUI程序的调试

    app = QtWidgets.QApplication(sys.argv)  # 收集命令行的参数，为运行做准备

    mainWindow = QtWidgets.QMainWindow()  # 它是程序所显示的主界面
    ui = WidgetWindow(mainWindow)  # 实例化对象
    mainWindow.show()  # 在屏幕上显示

    sys.exit(app.exec_())  # 退出时把程序清理干净
