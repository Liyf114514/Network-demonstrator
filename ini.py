# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ini.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1328, 859)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(480, 690, 311, 91))
        self.pushButton.setObjectName("pushButton")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(260, 120, 781, 521))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.widget)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinBox_2 = QtWidgets.QSpinBox(self.widget)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_2.addWidget(self.spinBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_7.addWidget(self.label_3)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.horizontalLayout_7.addWidget(self.doubleSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_4.setObjectName("doubleSpinBox_4")
        self.horizontalLayout_6.addWidget(self.doubleSpinBox_4)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout_4.addWidget(self.textEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1328, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.accepted)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "initialize!"))
        self.label.setText(_translate("MainWindow", "Total channels"))
        self.label_2.setText(_translate("MainWindow", "sector angle (in degrees)"))
        self.label_3.setText(_translate("MainWindow", "user speed"))
        self.label_7.setText(_translate("MainWindow", "car speed"))
        self.label_4.setText(_translate("MainWindow", "filepath"))

    def accepted(self):
        try:
            # 获取 spinbox 的值
            channel = self.spinBox.value()
            sector = self.spinBox_2.value()
            users = self.doubleSpinBox.value()
            cars = self.doubleSpinBox_4.value()
            temp = self.textEdit.toPlainText()
            # 检查内容是否为空
            if not temp.strip():  # 使用 .strip() 来检查实质性的空内容（即使只有空格也算空）
                # 如果为空，则存储默认内容
                temp = "default"  # 这里替换为您想要的默认内容
                file_name_png = temp + ".png"  # 添加 .png 扩展名
                file_name_txt = temp + ".txt"  # 添加 .txt 扩展名
            else:
                # 如果不为空，在 temp 后加上 .png 和 .txt 格式
                file_name_png = temp + ".png"
                file_name_txt = temp + ".txt"

            filename = 'initial.txt'
            print(channel,sector,users,cars,file_name_png,file_name_txt)
            with open(filename, 'w') as file:
                file.write(f"{channel},{sector},{users},{cars},{file_name_png},{file_name_txt}\n")
        except Exception as e:
            print(f"发生错误: {e}")


def main():
    app = QtWidgets.QApplication(sys.argv)

    # 创建一个 QDialog 实例
    QMW = QtWidgets.QMainWindow()

    # 创建 Ui_Dialog 实例
    ui = Ui_MainWindow()

    # 设置 QDialog 的 UI
    ui.setupUi(QMW)

    # 显示 QDialog 实例
    QMW.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

    # 关闭对话框
    QtCore.QCoreApplication.instance().quit()