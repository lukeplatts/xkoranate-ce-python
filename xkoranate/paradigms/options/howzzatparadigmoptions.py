from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QGridLayout, QStyle

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toString


class XkorHowzzatParadigmOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.homeAdvantage = QCheckBox("Apply home advantage")
        if toString(self.options.get("homeAdvantage")) == "true":
            self.homeAdvantage.setCheckState(Qt.Checked)
        else:
            self.homeAdvantage.setCheckState(Qt.Unchecked)
        self.setHomeAdvantage(self.homeAdvantage.checkState())
        self.homeAdvantage.stateChanged.connect(self.setHomeAdvantage)

        self.useStyleMods = QCheckBox("Apply style modifiers")
        if toString(self.options.get("useStyleMods", "true")) == "true":
            self.useStyleMods.setCheckState(Qt.Checked)
        else:
            self.useStyleMods.setCheckState(Qt.Unchecked)
        self.setUseStyleMods(self.useStyleMods.checkState())
        self.useStyleMods.stateChanged.connect(self.setUseStyleMods)

        self.showTLAs = QCheckBox("Show team names")
        if toString(self.options.get("showTLAs", "true")) == "true":
            self.showTLAs.setCheckState(Qt.Checked)
        else:
            self.showTLAs.setCheckState(Qt.Unchecked)
        self.setShowTLAs(self.showTLAs.checkState())
        self.showTLAs.stateChanged.connect(self.setShowTLAs)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.homeAdvantage, 0, 1)
        self.layout.addWidget(self.useStyleMods, 1, 1)
        self.layout.addWidget(self.showTLAs, 2, 1)
        self.layout.setHorizontalSpacing(0)
        if Qt.AlignmentFlag(self.style().styleHint(QStyle.SH_FormLayoutFormAlignment)) & Qt.AlignHCenter:
            # center the check boxes, but leave them left-aligned with each other on Mac OS
            self.layout.setColumnStretch(0, 1093)
            self.layout.setColumnStretch(2, 1093)

    def setHomeAdvantage(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["homeAdvantage"] = "true"
        else:
            self.options["homeAdvantage"] = "false"
        self.optionsChanged.emit(self.options)

    def setShowTLAs(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["showTLAs"] = "true"
        else:
            self.options["showTLAs"] = "false"
        self.optionsChanged.emit(self.options)

    def setUseStyleMods(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["useStyleMods"] = "true"
        else:
            self.options["useStyleMods"] = "false"
        self.optionsChanged.emit(self.options)
