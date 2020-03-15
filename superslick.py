# coding: utf-8

import subprocess
import os
import pathlib

from sys import exit, argv
from PySide2 import QtWidgets, QtCore, QtGui

from wrapped_qt import QIconLabel


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("すべすべオイル")
        self.setWindowIcon(
            QtGui.QIcon(QtGui.QPixmap(os.path.abspath("./resources/superslick.ico")))
        )

        hbox = QtWidgets.QHBoxLayout()
        qtab = QtWidgets.QTabWidget()

        wid = Contents_Grid_Widget(
            [
                {
                    "title": "Autodesk Maya",
                    "installer": "./batch/test.bat",
                    "description": "Autodesk Mayaのインストールと各種セットアップを行います。",
                    "icon": "./resources/Maya.png"
                },
                {
                    "title": "Zbrush",
                    "description": "Zbrushのインストールを行います。",
                    "icon": "./resources/ZBrush.png"
                },
                {
                    "title": "Substance Designer",
                    "description": "Substance Designerのインストールを行います。",
                    "icon": "./resources/substanceDesigner.png"
                },
                {
                    "title": "Substance Painter",
                    "description": "Substance Painterのインストールを行います。",
                    "icon": "./resources/SubstancePainter.png"
                },
                {
                    "title": "World Machine",
                    "description": "World Machineのインストールを行います。",
                    "icon": "./resources/worldMachine.png"
                },
                {
                    "title": "Houdini",
                    "description": "Houdiniと各種セットアップのインストールを行います。",
                    "icon": "./resources/Houdini.png"
                },
            ]
        )

        wid2 = Contents_Grid_Widget(
            [
                {
                    "title": "Maya",
                    "installer": "./batch/test.bat",
                    "description": "testppppppppppppppppppppppppp",
                },
                {"title": "Zbrush", "description": "testppppppppppppppppppppppppp"},
            ]
        )

        qtab.addTab(wid, "DCC Tools")
        qtab.addTab(wid2, "Windows")
        qtab.addTab(QtWidgets.QWidget(), "Log")

        hbox.addWidget(qtab)
        self.setLayout(hbox)


class Content_Widget(QtWidgets.QWidget):
    def __init__(
        self,
        title="",
        description="",
        icon="./resources/placeholder.png",
        installer="",
        validator="",
    ):
        super().__init__()
        print(title, description, icon, validator, installer)

        self.installer = os.path.abspath(installer) if installer else ""
        self.validator = os.path.abspath(validator) if validator else ""

        self.setFixedHeight(128 + 36)
        title_widget = QtWidgets.QLabel("")
        title_widget.setText(title)
        title_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )

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

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.init(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, painter, self)


class Contents_Grid_Widget(QtWidgets.QWidget):
    def __init__(self, contents=[]):
        super().__init__()

        grid = QtWidgets.QGridLayout()
        for i, content in enumerate(contents):
            grid.addWidget(Content_Widget(**content), i // 2, i % 2)

        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)


class Install_Button_Widget(QtWidgets.QPushButton):
    def __init__(self, installer="", validator=""):
        super().__init__()
        self.installer = installer
        self.validator = validator

        self.setText("Install")
        self.setFixedWidth(120)
        self.clicked.connect(self.install)
        self.validate()

    def install(self):
        self.setEnabled(False)
        try:
            subprocess.check_output([self.installer])
            self.succuess()
        except subprocess.CalledProcessError:
            self.error()

    def error(self):
        self.setText("Install Failed")
        self.setStyleSheet("background:#D33;color:white;")
        self.parentWidget().setEnabled(False)

    def succuess(self):
        self.setText("Installed")
        self.parentWidget().setEnabled(False)

    def validate(self):
        if self.installer == "":
            self.setText("Not set installer")
            self.setEnabled(False)
        elif not pathlib.Path(self.installer).exists():
            self.setText("Not found installer")
            self.setEnabled(False)

        if not self.validator:
            return
        elif not pathlib.Path(self.validator).exists():
            self.setEnabled(False)
            self.setText("Not found validator")


class Description_Widget(QtWidgets.QTextEdit):
    def __init__(self, text):
        super().__init__()

        self.setText(text)
        self.setMaximumHeight(128)
        self.setReadOnly(True)



def main():
    app = QtWidgets.QApplication(argv)

    window = Window()
    with open("./resources/style.css") as f:
        window.setStyleSheet(f.read())
    window.show()

    exec_result = app.exec_()

    exit(exec_result)


if __name__ == "__main__":
    main()
