# coding: utf-8

import subprocess
import os

from sys import exit, argv
from PySide2 import QtWidgets, QtCore, QtGui

from wrapped_qt import QIconLabel, QRectLabel

from collections import namedtuple

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        hbox = QtWidgets.QHBoxLayout()
        qtab = QtWidgets.QTabWidget()

        wid = Contents_Grid_Widget([
            {"title": "Title2", "installer": "./batch/test.bat"},
            {"title": "Title2"},
        ])

        qtab.addTab(wid, "Tab1")

        hbox.addWidget(qtab)
        self.setLayout(hbox)
        

class Content_Widget(QtWidgets.QWidget):
    def __init__(self, title="", description="", icon="./resources/placeholder.png", validater="", installer=""):
        super().__init__()
        self.setAutoFillBackground(True)
        # self.setStyleSheet("background-color:black;")
        # self.setBackgroundRole(QtGui.QPalette.dark)
        self.validater = os.path.abspath(validater) if os.path.exists(validater) else ""
        self.installer = os.path.abspath(installer) if os.path.exists(installer) else ""

        self.setFixedHeight(128+36)
        title_widget = QtWidgets.QLabel("")
        title_widget.setText(title)
        title_widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        description_widget = Description_Widget(description)

        icon_widget = QIconLabel(icon, (128, 128))
        button_widget = Install_Button_Widget(self.installer)

        sub_layout = QtWidgets.QVBoxLayout()
        sub_layout.addWidget(description_widget)
        sub_layout.addWidget(button_widget)
        sub_layout.setAlignment(button_widget, QtCore.Qt.AlignRight)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(icon_widget)
        main_layout.addLayout(sub_layout)

        top = QtWidgets.QVBoxLayout()
        top.addWidget(title_widget)
        top.addLayout(main_layout)

        self.setLayout(top)
        self.validate()

    def validate(self):
        pass


class Contents_Grid_Widget(QtWidgets.QWidget):
    def __init__(self, contents=[]):
        super().__init__()

        grid = QtWidgets.QGridLayout()
        for i, content in enumerate(contents):
            grid.addWidget(Content_Widget(**content), i // 2, i % 2)

        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)

class Install_Button_Widget(QtWidgets.QPushButton):
    def __init__(self, installer=""):
        super().__init__()
        self.installer = installer

        self.setText("Install")
        self.setFixedWidth(60)
        self.clicked.connect(self.install)

    def install(self):
        if not self.installer:
            return

        try:
            self.setEnabled(False)
            subprocess.check_output([self.installer])
        except subprocess.CalledProcessError:
            print("Error")
            self.parentWidget().setStyleSheet('background-color:red;')
        finally:
            self.setEnabled(True)
            



class Description_Widget(QtWidgets.QTextEdit):
    def __init__(self, text):
        super().__init__()

        self.setText(text)
        self.setMaximumHeight(128)
        self.setReadOnly(True)

class Logger_Layout():
    pass

def main():
    app = QtWidgets.QApplication(argv)

    window = Window()
    window.show()

    exec_result = app.exec_()

    exit(exec_result)


if __name__ == "__main__":
    main()
