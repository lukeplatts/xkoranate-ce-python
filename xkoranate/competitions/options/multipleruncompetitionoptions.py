from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QFormLayout, QGridLayout, QSpinBox, QStyle

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toInt, toString


class XkorMultipleRunCompetitionOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.runs = QSpinBox()
        self.runs.setValue(toInt(self.options.get("runs", 2)))
        self.runs.setRange(2, 99)
        self.runs.valueChanged.connect(self.setRuns)

        self.sortResults = QCheckBox("Sort results")
        if toString(self.options.get("sortResults", "true")) == "true":
            self.sortResults.setCheckState(Qt.CheckState.Checked)
        self.sortResults.stateChanged.connect(self.setSortResults)

        self.sortByBestResult = QCheckBox("Sort by best result when total result is tied")
        if toString(self.options.get("sortByBestResult", "true")) == "true":
            self.sortByBestResult.setCheckState(Qt.CheckState.Checked)
        self.sortByBestResult.setEnabled(self.sortResults.checkState() == Qt.CheckState.Checked)
        self.sortByBestResult.stateChanged.connect(self.setSortByBestResult)

        form = QFormLayout()
        form.addRow("Runs:", self.runs)

        layout = QGridLayout(self)
        layout.addLayout(form, 0, 1)
        layout.addWidget(self.sortResults, 1, 1)
        layout.addWidget(self.sortByBestResult, 2, 1)
        layout.setHorizontalSpacing(0)
        if self.style().styleHint(QStyle.StyleHint.SH_FormLayoutFormAlignment) & Qt.AlignmentFlag.AlignHCenter.value:
            # center the check boxes, but leave them left-aligned with each other on Mac OS
            layout.setColumnStretch(0, 1093)
            layout.setColumnStretch(2, 1093)

    def setRuns(self, value):
        self.options["runs"] = value
        self.optionsChanged.emit(self.options)

    def setSortByBestResult(self, value):
        if isinstance(value, Qt.CheckState):
            value = value.value
        if value == Qt.CheckState.Checked.value:
            self.options["sortByBestResult"] = "true"
        else:
            self.options["sortByBestResult"] = "false"
        self.optionsChanged.emit(self.options)

    def setSortResults(self, value):
        if isinstance(value, Qt.CheckState):
            value = value.value
        if value == Qt.CheckState.Checked.value:
            self.options["sortResults"] = "true"
            self.sortByBestResult.setEnabled(True)
            self.setSortByBestResult(self.sortByBestResult.checkState())
        else:
            self.options["sortResults"] = "false"
            self.sortByBestResult.setEnabled(False)
            self.options["sortByBestResult"] = "false"
        self.optionsChanged.emit(self.options)
