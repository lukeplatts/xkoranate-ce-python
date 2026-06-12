from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QGridLayout, QStyle

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toString


class XkorShortTrackParadigmOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.showTLAs = QCheckBox("Show team names")
        if toString(self.options.get("showTLAs")) == "false":
            self.showTLAs.setCheckState(Qt.Unchecked)
        else:
            self.showTLAs.setCheckState(Qt.Checked)
        self.setShowTLAs(self.showTLAs.checkState())
        self.showTLAs.stateChanged.connect(self.setShowTLAs)

        self.allowAdvancement = QCheckBox("Allow athletes to be advanced")
        if toString(self.options.get("allowAdvancement")) == "false":
            self.allowAdvancement.setCheckState(Qt.Unchecked)
        else:
            self.allowAdvancement.setCheckState(Qt.Checked)
        self.setAllowAdvancement(self.allowAdvancement.checkState())
        self.allowAdvancement.stateChanged.connect(self.setAllowAdvancement)

        # layout
        layout = QGridLayout(self)
        layout.addWidget(self.showTLAs, 0, 1)
        layout.addWidget(self.allowAdvancement, 1, 1)
        layout.setHorizontalSpacing(0)
        if Qt.AlignmentFlag(self.style().styleHint(QStyle.SH_FormLayoutFormAlignment)) & Qt.AlignHCenter:
            # center the check boxes, but leave them left-aligned with each other on Mac OS
            layout.setColumnStretch(0, 1093)
            layout.setColumnStretch(2, 1093)

    def setAllowAdvancement(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["allowAdvancement"] = "true"
        else:
            self.options["allowAdvancement"] = "false"
        self.optionsChanged.emit(self.options)

    def setShowTLAs(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["showTLAs"] = "true"
        else:
            self.options["showTLAs"] = "false"
        self.optionsChanged.emit(self.options)
