from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QButtonGroup, QCheckBox, QDoubleSpinBox,
                               QFormLayout, QHBoxLayout, QLabel, QPushButton,
                               QRadioButton, QWidget)

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toDouble, toString

_DEFAULT_HOME_ADVANTAGE_MAGNITUDE = 4.0 / 3.0


class XkorNSFSParadigmOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, defaultHomeAdvantageMagnitude=_DEFAULT_HOME_ADVANTAGE_MAGNITUDE, parent=None):
        super().__init__(opts, parent)
        self._defaultHomeAdvantageMagnitude = defaultHomeAdvantageMagnitude

        self.homeAdvantage = QCheckBox("Apply home advantage")
        if toString(self.options.get("homeAdvantage")) == "true":
            self.homeAdvantage.setCheckState(Qt.Checked)
        self.setHomeAdvantage(self.homeAdvantage.checkState())
        self.homeAdvantage.stateChanged.connect(self.setHomeAdvantage)

        self.homeAdvantageMagnitudeLabel = QLabel("Home advantage magnitude:")
        self.homeAdvantageMagnitude = QDoubleSpinBox()
        self.homeAdvantageMagnitude.setDecimals(3)
        self.homeAdvantageMagnitude.setRange(0, 5)
        self.homeAdvantageMagnitude.setSingleStep(0.05)
        self.homeAdvantageMagnitude.setValue(toDouble(self.options.get(
            "homeAdvantageMagnitude", defaultHomeAdvantageMagnitude)))
        self.setHomeAdvantageMagnitude(self.homeAdvantageMagnitude.value())
        self.homeAdvantageMagnitude.valueChanged.connect(self.setHomeAdvantageMagnitude)

        self.restoreHomeAdvantageMagnitude = QPushButton("Restore default")
        self.restoreHomeAdvantageMagnitude.setToolTip(
            "Reset to this sport's configured value (%.3f)" % defaultHomeAdvantageMagnitude)
        self.restoreHomeAdvantageMagnitude.clicked.connect(self._restoreHomeAdvantageMagnitude)

        self._updateHomeAdvantageMagnitudeEnabled(self.homeAdvantage.checkState())
        self.homeAdvantage.stateChanged.connect(self._updateHomeAdvantageMagnitudeEnabled)

        self.homeAdvantageMagnitudeRow = QWidget()
        homeAdvantageMagnitudeRowLayout = QHBoxLayout(self.homeAdvantageMagnitudeRow)
        homeAdvantageMagnitudeRowLayout.setContentsMargins(0, 0, 0, 0)
        homeAdvantageMagnitudeRowLayout.addWidget(self.homeAdvantageMagnitude)
        homeAdvantageMagnitudeRowLayout.addWidget(self.restoreHomeAdvantageMagnitude)

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
        form.addRow(self.homeAdvantageMagnitudeLabel, self.homeAdvantageMagnitudeRow)
        form.addRow("", self.showTLAs)
        form.addRow(label, styleModsForm)

    def setHomeAdvantage(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["homeAdvantage"] = "true"
        else:
            self.options["homeAdvantage"] = "false"
        self.optionsChanged.emit(self.options)

    def setHomeAdvantageMagnitude(self, x):
        self.options["homeAdvantageMagnitude"] = x
        self.optionsChanged.emit(self.options)

    def _restoreHomeAdvantageMagnitude(self):
        self.homeAdvantageMagnitude.setValue(self._defaultHomeAdvantageMagnitude)

    def _updateHomeAdvantageMagnitudeEnabled(self, x):
        enabled = Qt.CheckState(x) == Qt.Checked
        self.homeAdvantageMagnitudeLabel.setEnabled(enabled)
        self.homeAdvantageMagnitude.setEnabled(enabled)
        self.restoreHomeAdvantageMagnitude.setEnabled(enabled)

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
