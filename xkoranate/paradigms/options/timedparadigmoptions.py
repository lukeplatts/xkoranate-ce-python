from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QGridLayout, QStyle

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toString


class XkorTimedParadigmOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.showTLAs = QCheckBox("Show team names")
        if toString(self.options.get("showTLAs")) == "false":
            self.showTLAs.setCheckState(Qt.Unchecked)
        else:
            self.showTLAs.setCheckState(Qt.Checked)
        self.setShowTLAs(self.showTLAs.checkState())
        self.showTLAs.stateChanged.connect(self.setShowTLAs)

        # layout
        layout = QGridLayout(self)
        layout.addWidget(self.showTLAs, 0, 0, Qt.AlignmentFlag(self.style().styleHint(QStyle.SH_FormLayoutFormAlignment)))

    def setShowTLAs(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["showTLAs"] = "true"
        else:
            self.options["showTLAs"] = "false"
        self.optionsChanged.emit(self.options)
