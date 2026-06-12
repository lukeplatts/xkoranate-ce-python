from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QGridLayout, QStyle

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toString


class XkorNSFSGridironParadigmOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.usePeriods = QCheckBox("Show period-by-period results")
        if toString(self.options.get("usePeriods", "true")) == "true":
            self.usePeriods.setCheckState(Qt.Checked)
        self.setUsePeriods(self.usePeriods.checkState())
        self.usePeriods.stateChanged.connect(self.setUsePeriods)

        self.showTLAs = QCheckBox("Show team names")
        if toString(self.options.get("showTLAs", "true")) == "true":
            self.showTLAs.setCheckState(Qt.Checked)
        self.setShowTLAs(self.showTLAs.checkState())
        self.showTLAs.stateChanged.connect(self.setShowTLAs)

        # layout
        layout = QGridLayout(self)
        layout.addWidget(self.usePeriods, 0, 1)
        layout.addWidget(self.showTLAs, 1, 1)
        layout.setHorizontalSpacing(0)
        if Qt.AlignmentFlag(self.style().styleHint(QStyle.SH_FormLayoutFormAlignment)) & Qt.AlignHCenter:
            # center the check boxes, but leave them left-aligned with each other on Mac OS
            layout.setColumnStretch(0, 1093)
            layout.setColumnStretch(2, 1093)

    def setShowTLAs(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["showTLAs"] = "true"
        else:
            self.options["showTLAs"] = "false"
        self.optionsChanged.emit(self.options)

    def setUsePeriods(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["usePeriods"] = "true"
        else:
            self.options["usePeriods"] = "false"
        self.optionsChanged.emit(self.options)
