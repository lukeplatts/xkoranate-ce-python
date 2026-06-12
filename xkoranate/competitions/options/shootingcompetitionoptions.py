from PySide6.QtWidgets import QFormLayout, QGridLayout, QLabel, QSpinBox

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toInt


class XkorShootingCompetitionOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.cutoff = QSpinBox()
        self.cutoff.setMinimum(0)
        self.cutoff.setMaximum(999)
        self.cutoff.setSpecialValueText("all")
        if "cutoff" in self.options:
            self.cutoff.setValue(toInt(self.options.get("cutoff")))
        self.cutoff.valueChanged.connect(self.setCutoff)

        self.explanation = QLabel("<small>In the qualifying round, all ties will be unresolved.<br/>In the final round, only ties for medal positions will be settled by shoot-offs.</small>")
        self.explanation.setWordWrap(True)

        form = QFormLayout()
        form.addRow("Shooters advancing to final", self.cutoff)

        layout = QGridLayout(self)
        layout.addLayout(form, 0, 0)
        layout.addWidget(self.explanation, 1, 0)

    def setCutoff(self, value):
        if value == 0:
            self.explanation.setText("<small>In the qualifying round, all ties will be left unresolved.<br/>In the final round, only ties for medal positions will be settled by shoot-offs.</small>")
        elif value % 10 == 1 and value != 11:
            self.explanation.setText("<small>In the qualifying round, only a tie for %dst place will be settled by a shoot-off.<br/>In the final round, only ties for medal positions will be settled by shoot-offs.</small>" % value)
        elif value % 10 == 2 and value != 12:
            self.explanation.setText("<small>In the qualifying round, only a tie for %dnd place will be settled by a shoot-off.<br/>In the final round, only ties for medal positions will be settled by shoot-offs.</small>" % value)
        elif value % 10 == 3 and value != 13:
            self.explanation.setText("<small>In the qualifying round, only a tie for %drd place will be settled by a shoot-off.<br/>In the final round, only ties for medal positions will be settled by shoot-offs.</small>" % value)
        else:
            self.explanation.setText("<small>In the qualifying round, only a tie for %dth place will be settled by a shoot-off.<br/>In the final round, only ties for medal positions will be settled by shoot-offs.</small>" % value)
        self.options["cutoff"] = value
        self.optionsChanged.emit(self.options)
