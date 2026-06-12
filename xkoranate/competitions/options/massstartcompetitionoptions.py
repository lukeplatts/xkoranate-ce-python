from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QGridLayout, QStyle

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toString


class XkorMassStartCompetitionOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.overallRanking = QCheckBox("Show overall ranking across all groups")
        if toString(self.options.get("overallRanking", "false")) == "true":
            self.overallRanking.setCheckState(Qt.CheckState.Checked)
        self.overallRanking.stateChanged.connect(self.setOverallRanking)

        self.sortResults = QCheckBox("Sort results")
        if toString(self.options.get("sortResults", "true")) == "true":
            self.sortResults.setCheckState(Qt.CheckState.Checked)
        self.sortResults.stateChanged.connect(self.setSortResults)

        layout = QGridLayout(self)
        layout.addWidget(self.sortResults, 0, 1)
        layout.addWidget(self.overallRanking, 1, 1)
        layout.setHorizontalSpacing(0)
        if self.style().styleHint(QStyle.StyleHint.SH_FormLayoutFormAlignment) & Qt.AlignmentFlag.AlignHCenter.value:
            # center the check boxes, but leave them left-aligned with each other on Mac OS
            layout.setColumnStretch(0, 1093)
            layout.setColumnStretch(2, 1093)

    def setOverallRanking(self, value):
        if isinstance(value, Qt.CheckState):
            value = value.value
        if value == Qt.CheckState.Checked.value:
            self.options["overallRanking"] = "true"
        else:
            self.options["overallRanking"] = "false"
        self.optionsChanged.emit(self.options)

    def setSortResults(self, value):
        if isinstance(value, Qt.CheckState):
            value = value.value
        if value == Qt.CheckState.Checked.value:
            self.options["sortResults"] = "true"
            self.overallRanking.setEnabled(True)
            self.setOverallRanking(self.overallRanking.checkState())
        else:
            self.options["sortResults"] = "false"
            self.overallRanking.setEnabled(False)
            self.options["overallRanking"] = "false"
        self.optionsChanged.emit(self.options)
