from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QCheckBox, QDoubleSpinBox, QFormLayout,
                               QGridLayout, QStyle)

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toDouble, toString


class XkorPGSParadigmOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.showTLAs = QCheckBox("Show team names")
        if toString(self.options.get("showTLAs")) == "false":
            self.showTLAs.setCheckState(Qt.Unchecked)
        else:
            self.showTLAs.setCheckState(Qt.Checked)
        self.setShowTLAs(self.showTLAs.checkState())
        self.showTLAs.stateChanged.connect(self.setShowTLAs)

        self.maxScore = QDoubleSpinBox()
        self.maxScore.setRange(0, 1.5)
        self.maxScore.setSingleStep(0.01)
        self.maxScore.setValue(toDouble(self.options.get("maxScore", 1.5)))
        self.maxScore.valueChanged.connect(self.setMaxScore)

        form = QFormLayout()
        form.addRow("Maximum score after first run:", self.maxScore)

        layout = QGridLayout(self)
        layout.addWidget(self.showTLAs, 0, 0, Qt.AlignmentFlag(self.style().styleHint(QStyle.SH_FormLayoutFormAlignment)))
        layout.addLayout(form, 1, 0)

    def setMaxScore(self, x):
        self.options["maxScore"] = x
        self.optionsChanged.emit(self.options)

    def setShowTLAs(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["showTLAs"] = "true"
        else:
            self.options["showTLAs"] = "false"
        self.optionsChanged.emit(self.options)
