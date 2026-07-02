from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QDoubleSpinBox, QGridLayout, QLabel, QStyle

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toDouble, toString

_DEFAULT_HOME_ADVANTAGE_MAGNITUDE = 0.065


class XkorFootba11erParadigmOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.homeAdvantage = QCheckBox("Apply home advantage")
        if toString(self.options.get("homeAdvantage")) == "true":
            self.homeAdvantage.setCheckState(Qt.Checked)
        else:
            self.homeAdvantage.setCheckState(Qt.Unchecked)
        self.setHomeAdvantage(self.homeAdvantage.checkState())
        self.homeAdvantage.stateChanged.connect(self.setHomeAdvantage)

        self.homeAdvantageMagnitudeLabel = QLabel("Home advantage magnitude:")
        self.homeAdvantageMagnitude = QDoubleSpinBox()
        self.homeAdvantageMagnitude.setDecimals(3)
        self.homeAdvantageMagnitude.setRange(-1, 1)
        self.homeAdvantageMagnitude.setSingleStep(0.005)
        self.homeAdvantageMagnitude.setValue(toDouble(self.options.get(
            "homeAdvantageMagnitude", _DEFAULT_HOME_ADVANTAGE_MAGNITUDE)))
        self.setHomeAdvantageMagnitude(self.homeAdvantageMagnitude.value())
        self.homeAdvantageMagnitude.valueChanged.connect(self.setHomeAdvantageMagnitude)
        self._updateHomeAdvantageMagnitudeEnabled(self.homeAdvantage.checkState())
        self.homeAdvantage.stateChanged.connect(self._updateHomeAdvantageMagnitudeEnabled)

        self.showTLAs = QCheckBox("Show team names")
        if toString(self.options.get("showTLAs", "true")) == "true":
            self.showTLAs.setCheckState(Qt.Checked)
        else:
            self.showTLAs.setCheckState(Qt.Unchecked)
        self.setShowTLAs(self.showTLAs.checkState())
        self.showTLAs.stateChanged.connect(self.setShowTLAs)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.homeAdvantage, 0, 1)
        self.layout.addWidget(self.homeAdvantageMagnitudeLabel, 1, 0, Qt.AlignRight)
        self.layout.addWidget(self.homeAdvantageMagnitude, 1, 1)
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

    def setHomeAdvantageMagnitude(self, x):
        self.options["homeAdvantageMagnitude"] = x
        self.optionsChanged.emit(self.options)

    def _updateHomeAdvantageMagnitudeEnabled(self, x):
        enabled = Qt.CheckState(x) == Qt.Checked
        self.homeAdvantageMagnitudeLabel.setEnabled(enabled)
        self.homeAdvantageMagnitude.setEnabled(enabled)

    def setShowTLAs(self, x):
        if Qt.CheckState(x) == Qt.Checked:
            self.options["showTLAs"] = "true"
        else:
            self.options["showTLAs"] = "false"
        self.optionsChanged.emit(self.options)
