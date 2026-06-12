from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QSplitter, QSplitterHandle


class XkorThinSplitterHandle(QSplitterHandle):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.palette().dark().color())
        painter.drawLine(0, 0, 0, self.height())

    def sizeHint(self):
        return QSize(1, QSplitterHandle.sizeHint(self).height())


class XkorThinSplitter(QSplitter):
    def createHandle(self):
        return XkorThinSplitterHandle(self.orientation(), self)
