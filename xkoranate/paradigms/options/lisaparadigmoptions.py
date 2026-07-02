from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QCheckBox, QDoubleSpinBox, QFormLayout,
                               QHBoxLayout, QLabel, QPushButton, QWidget)

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toDouble, toString

_DEFAULT_HOME_ADVANTAGE_EAR = 100.0


class XkorLISAParadigmOptions(XkorAbstractOptionsWidget):
    """Per-event overrides for LISA. Most of the tunable constants the
    algorithm's author calls out as adjustable (power scalar, REAR, margin
    divisor) are sport-file constants edited in the XML, matching how
    NSFS/SQIS keep their numeric coefficients XML-only; home-advantage
    magnitude is the exception, surfaced here the same way NSFS/Footba11er
    surface theirs."""

    def __init__(self, opts, defaultHomeAdvantageEAR=_DEFAULT_HOME_ADVANTAGE_EAR, parent=None):
        super().__init__(opts, parent)
        self._defaultHomeAdvantageEAR = defaultHomeAdvantageEAR

        self.homeAdvantage = QCheckBox("Apply home advantage")
        if toString(self.options.get("homeAdvantage")) == "true":
            self.homeAdvantage.setCheckState(Qt.Checked)
        else:
            self.homeAdvantage.setCheckState(Qt.Unchecked)
        self.setHomeAdvantage(self.homeAdvantage.checkState())
        self.homeAdvantage.stateChanged.connect(self.setHomeAdvantage)

        self.homeAdvantageEARLabel = QLabel("Home advantage (EAR):")
        self.homeAdvantageEAR = QDoubleSpinBox()
        self.homeAdvantageEAR.setDecimals(1)
        self.homeAdvantageEAR.setRange(0, 500)
        self.homeAdvantageEAR.setSingleStep(5)
        self.homeAdvantageEAR.setValue(toDouble(self.options.get(
            "homeAdvantageEAR", defaultHomeAdvantageEAR)))
        self.setHomeAdvantageEAR(self.homeAdvantageEAR.value())
        self.homeAdvantageEAR.valueChanged.connect(self.setHomeAdvantageEAR)

        self.restoreHomeAdvantageEAR = QPushButton("Restore default")
        self.restoreHomeAdvantageEAR.setToolTip(
            "Reset to this sport's configured value (%.1f)" % defaultHomeAdvantageEAR)
        self.restoreHomeAdvantageEAR.clicked.connect(self._restoreHomeAdvantageEAR)

        self._updateHomeAdvantageEAREnabled(self.homeAdvantage.checkState())
        self.homeAdvantage.stateChanged.connect(self._updateHomeAdvantageEAREnabled)

        self.homeAdvantageEARRow = QWidget()
        homeAdvantageEARRowLayout = QHBoxLayout(self.homeAdvantageEARRow)
        homeAdvantageEARRowLayout.setContentsMargins(0, 0, 0, 0)
        homeAdvantageEARRowLayout.addWidget(self.homeAdvantageEAR)
        homeAdvantageEARRowLayout.addWidget(self.restoreHomeAdvantageEAR)

        self.showTLAs = QCheckBox("Show team names")
        if toString(self.options.get("showTLAs", "true")) == "true":
            self.showTLAs.setCheckState(Qt.Checked)
        else:
            self.showTLAs.setCheckState(Qt.Unchecked)
        self.setShowTLAs(self.showTLAs.checkState())
        self.showTLAs.stateChanged.connect(self.setShowTLAs)

        form = QFormLayout(self)
        form.addRow("", self.homeAdvantage)
        form.addRow(self.homeAdvantageEARLabel, self.homeAdvantageEARRow)
        form.addRow("", self.showTLAs)

    def setHomeAdvantage(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["homeAdvantage"] = "true"
        else:
            self.options["homeAdvantage"] = "false"
        self.optionsChanged.emit(self.options)

    def setHomeAdvantageEAR(self, x):
        self.options["homeAdvantageEAR"] = x
        self.optionsChanged.emit(self.options)

    def _restoreHomeAdvantageEAR(self):
        self.homeAdvantageEAR.setValue(self._defaultHomeAdvantageEAR)

    def _updateHomeAdvantageEAREnabled(self, x):
        enabled = Qt.CheckState(x) == Qt.Checked
        self.homeAdvantageEARLabel.setEnabled(enabled)
        self.homeAdvantageEAR.setEnabled(enabled)
        self.restoreHomeAdvantageEAR.setEnabled(enabled)

    def setShowTLAs(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["showTLAs"] = "true"
        else:
            self.options["showTLAs"] = "false"
        self.optionsChanged.emit(self.options)
