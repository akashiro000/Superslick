# coding: utf-8

import subprocess
import os
import pathlib

from sys import exit, argv
from PySide2 import QtWidgets, QtCore, QtGui

from wrapped_qt import QIconLabel
from config import Config

import argparse
import json

global parsed_args
parsed_args = argparse.Namespace()


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("すべすべオイル")

        icon_path = Config.get("icon")["path"]
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(icon_path)))

        hbox = QtWidgets.QHBoxLayout()
        qtab = QtWidgets.QTabWidget()

        for tab in Config.get("tabs", []):
            title = tab.get("title")
            wid = Contents_Grid_Widget(tab.get("contents"))
            qtab.addTab(wid, title)

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
        self.button_widget = Install_Button_Widget(self.installer, self.validator)

        sub_layout = QtWidgets.QVBoxLayout()
        sub_layout.addWidget(description_widget)
        sub_layout.addWidget(self.button_widget)
        sub_layout.setAlignment(self.button_widget, QtCore.Qt.AlignRight)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(icon_widget)
        main_layout.addLayout(sub_layout)

        top = QtWidgets.QVBoxLayout()
        top.addWidget(title_widget)
        top.addLayout(main_layout)

        self.setLayout(top)
        self.validate()

    def validate(self):
        self.button_widget.validate()

    def paintEvent(self, event):
        opt = QtWidgets.QStyleOption()
        opt.init(self)
        style = self.style()
        style.drawPrimitive(QtWidgets.QStyle.PE_Widget, opt, QtGui.QPainter(self), self)


class Contents_Grid_Widget(QtWidgets.QWidget):
    def __init__(self, contents=[]):
        super().__init__()

        grid = QtWidgets.QGridLayout()
        for i, content in enumerate(contents):
            grid.addWidget(Content_Widget(**content), i // 2, i % 2)
        else:
            if i == 0:
                grid.addWidget(Content_Widget(**{"icon": ""}), 0, 1)

        grid.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(grid)


class Install_Button_Widget(QtWidgets.QPushButton):
    def __init__(self, installer="", validator=""):
        super().__init__()
        self.installer = installer
        self.validator = validator

        self.setText("セットアップ 開始")
        self.setFixedWidth(160)
        self.clicked.connect(self.install)

    def install(self):
        self.setEnabled(False)
        try:
            result = subprocess.check_output([self.installer])
            self.succuess("セットアップ 完了")
        except subprocess.CalledProcessError:
            self.error("セットアップ 失敗")

    def error(self, message=""):
        if message:
            self.setText(message)
        self.setStyleSheet("background:#900;color:white;")
        self.parentWidget().setEnabled(False)

    def succuess(self, message=""):
        if message:
            self.setText(message)
        self.setStyleSheet("background:#030;")
        self.parentWidget().setEnabled(False)

    def invalid(self, message=""):
        if message:
            self.setText(message)
        self.parentWidget().setEnabled(False)

    def validate(self):
        if self.installer == "":
            self.invalid("未設定")
        elif not pathlib.Path(self.installer).exists():
            self.error("インストーラーが見つかりません")

        if self.validator:
            if not pathlib.Path(self.validator).exists():
                self.error("validatorが見つかりません")
                return

            try:
                subprocess.check_output([self.validator])
                self.succuess("セットアップ 済み")
            except:
                pass


class Description_Widget(QtWidgets.QTextEdit):
    def __init__(self, text):
        super().__init__()

        self.setText(text)
        self.setMaximumHeight(128)
        self.setReadOnly(True)


def generate_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c", "--config", help="config.jsonのパス", default="./resouces/config.json"
    )
    parser.add_argument(
        "-l", "--log", help="ログをファイルとして出力する。出力するファイルのパス", default="./superslick.log"
    )

    return parser


def main():
    generate_parser().parse_args()
    app = QtWidgets.QApplication(argv)

    window = Window()
    with open("./resources/style.css") as f:
        window.setStyleSheet(f.read())
    window.show()

    exec_result = app.exec_()

    exit(exec_result)


if __name__ == "__main__":
    main()
