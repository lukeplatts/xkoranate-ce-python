from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QFormLayout

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toString


class XkorLISAParadigmOptions(XkorAbstractOptionsWidget):
    """Per-event overrides for LISA. The tunable constants the algorithm's
    author calls out as adjustable (power scalar, REAR, margin divisor,
    home-advantage magnitude) are sport-file constants edited in the XML,
    matching how NSFS/SQIS keep their numeric coefficients XML-only; this
    widget only surfaces the same kind of per-event toggles those paradigms
    expose."""

    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.homeAdvantage = QCheckBox("Apply home advantage")
        if toString(self.options.get("homeAdvantage")) == "true":
            self.homeAdvantage.setCheckState(Qt.Checked)
        else:
            self.homeAdvantage.setCheckState(Qt.Unchecked)
        self.setHomeAdvantage(self.homeAdvantage.checkState())
        self.homeAdvantage.stateChanged.connect(self.setHomeAdvantage)

        self.showTLAs = QCheckBox("Show team names")
        if toString(self.options.get("showTLAs", "true")) == "true":
            self.showTLAs.setCheckState(Qt.Checked)
        else:
            self.showTLAs.setCheckState(Qt.Unchecked)
        self.setShowTLAs(self.showTLAs.checkState())
        self.showTLAs.stateChanged.connect(self.setShowTLAs)

        form = QFormLayout(self)
        form.addRow("", self.homeAdvantage)
        form.addRow("", self.showTLAs)

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
