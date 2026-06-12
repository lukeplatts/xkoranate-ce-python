from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QButtonGroup, QCheckBox, QFormLayout, QLabel,
                               QRadioButton)

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toString


class XkorNSFSParadigmOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.homeAdvantage = QCheckBox("Apply home advantage")
        if toString(self.options.get("homeAdvantage")) == "true":
            self.homeAdvantage.setCheckState(Qt.Checked)
        self.setHomeAdvantage(self.homeAdvantage.checkState())
        self.homeAdvantage.stateChanged.connect(self.setHomeAdvantage)

        self.showTLAs = QCheckBox("Show team names")
        if toString(self.options.get("showTLAs", "true")) == "true":
            self.showTLAs.setCheckState(Qt.Checked)
        self.setShowTLAs(self.showTLAs.checkState())
        self.showTLAs.stateChanged.connect(self.setShowTLAs)

        # style modifiers options
        self.xkorStyleMods = QRadioButton("xkoranate-style (additive)")
        self.nsfsStyleMods = QRadioButton("NSFS3-style (multiplicative)")
        self.noStyleMods = QRadioButton("Disable style modifiers")
        if toString(self.options.get("NSFSStyleMods")) != "false":
            self.nsfsStyleMods.setChecked(True)
        elif toString(self.options.get("styleMods")) == "true":
            self.xkorStyleMods.setChecked(True)
        else:
            self.noStyleMods.setChecked(True)
        self.styleMods = QButtonGroup()
        self.styleMods.addButton(self.xkorStyleMods)
        self.styleMods.addButton(self.nsfsStyleMods)
        self.styleMods.addButton(self.noStyleMods)
        self.styleMods.idClicked.connect(self.setStyleMods)

        styleModsForm = QFormLayout()
        styleModsForm.addRow(self.xkorStyleMods)
        styleModsForm.addRow(self.nsfsStyleMods)
        styleModsForm.addRow(self.noStyleMods)

        # QFormLayout sucks, so we create our own label
        label = QLabel("Style modifiers:")
        label.setContentsMargins(0, -4, 0, 0)

        form = QFormLayout(self)
        form.addRow("", self.homeAdvantage)
        form.addRow("", self.showTLAs)
        form.addRow(label, styleModsForm)

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

    def setStyleMods(self):
        checkedButton = self.styleMods.checkedButton()
        if checkedButton is self.nsfsStyleMods:
            self.options["styleMods"] = "false"
            self.options["NSFSStyleMods"] = "true"
        elif checkedButton is self.xkorStyleMods:
            self.options["styleMods"] = "true"
            self.options["NSFSStyleMods"] = "false"
        else:
            self.options["styleMods"] = "false"
            self.options["NSFSStyleMods"] = "false"
        self.optionsChanged.emit(self.options)
