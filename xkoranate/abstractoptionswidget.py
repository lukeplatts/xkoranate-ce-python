from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget


class XkorAbstractOptionsWidget(QWidget):
    optionsChanged = Signal(dict)

    def __init__(self, opts, parent=None):
        super().__init__(parent)
        self.options = dict(opts)

    def getOptions(self):
        return dict(self.options)

    def setOptions(self, newOptions):
        self.options = dict(newOptions)
        self.optionsChanged.emit(self.options)
