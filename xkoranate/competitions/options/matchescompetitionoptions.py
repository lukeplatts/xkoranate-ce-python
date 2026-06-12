from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QGridLayout, QStyle

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toString


class XkorMatchesCompetitionOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.allowDraws = QCheckBox("Allow draws")
        if "allowDraws" in self.options and toString(self.options.get("allowDraws")) == "false":
            self.allowDraws.setCheckState(Qt.CheckState.Unchecked)
        else:
            self.allowDraws.setCheckState(Qt.CheckState.Checked)
        self.allowDraws.stateChanged.connect(self.setAllowDraws)

        layout = QGridLayout(self)
        layout.addWidget(self.allowDraws, 0, 0, Qt.AlignmentFlag(self.style().styleHint(QStyle.StyleHint.SH_FormLayoutFormAlignment)))

    def setAllowDraws(self, value):
        if isinstance(value, Qt.CheckState):
            value = value.value
        if value == Qt.CheckState.Checked.value:
            self.options["allowDraws"] = "true"
        else:
            self.options["allowDraws"] = "false"
        self.optionsChanged.emit(self.options)
