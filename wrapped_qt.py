# coding: utf-8

from PySide2 import QtWidgets, QtGui, QtCore


class QIconLabel(QtWidgets.QLabel):
    COLOR = (30, 30, 30)
    OPACITY = 255 / 2

    CONSTRUCTED = False

    clicked = QtCore.Signal(QtGui.QMouseEvent)

    @classmethod
    def _construct(self):
        if self.CONSTRUCTED is False:
            self.overlay_pix = QtGui.QPixmap(QtCore.QSize(1, 1))
            self.overlay_pix.fill(QtGui.QColor(*self.COLOR, self.OPACITY))

            self.CONSTRUCTED = True

    def mousePressEvent(self, ev):
        self.clicked.emit(ev)

    def __init__(self, filename: str, size=(128, 128), overlay=False, *args, **kwargs):
        super(QIconLabel, self).__init__(*args, **kwargs)
        
        self._construct()

        self.filename = filename
        self.size = size
        self.overlay = overlay

        self.draw()

    def set_overlay(self, value=True):
        self.overlay = value
        self.draw()

    def draw(self):
        _pixmap = QtGui.QPixmap(self.filename)
        pixmap = _pixmap.scaled(*self.size, QtCore.Qt.KeepAspectRatio)

        if self.overlay:
            painter = QtGui.QPainter(pixmap)
            painter.drawPixmap(
                0, 0,
                self.overlay_pix.scaled(*self.size, QtCore.Qt.KeepAspectRatio),
            )
            painter.end()

        self.setPixmap(pixmap)

