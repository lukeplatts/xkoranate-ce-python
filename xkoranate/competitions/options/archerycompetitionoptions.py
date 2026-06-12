from PySide6.QtWidgets import QFormLayout, QGridLayout, QLabel, QSpinBox

from xkoranate.abstractoptionswidget import XkorAbstractOptionsWidget
from xkoranate.variant import toInt


class XkorArcheryCompetitionOptions(XkorAbstractOptionsWidget):
    def __init__(self, opts, parent=None):
        super().__init__(opts, parent)

        self.cutoff = QSpinBox()
        self.cutoff.setMinimum(0)
        self.cutoff.setMaximum(999)
        self.cutoff.setSpecialValueText("all")
        if "cutoff" in self.options:
            self.cutoff.setValue(toInt(self.options.get("cutoff")))
        self.cutoff.valueChanged.connect(self.setCutoff)

        self.explanation = QLabel("<small>All ties will be settled by lots.</small>")
        self.explanation.setWordWrap(True)

        form = QFormLayout()
        form.addRow("Archers advancing to next round", self.cutoff)

        layout = QGridLayout(self)
        layout.addLayout(form, 0, 0)
        layout.addWidget(self.explanation, 1, 0)

    def setCutoff(self, value):
        if value == 0:
            self.explanation.setText("<small>All ties will be settled by lots.</small>")
        elif value % 10 == 1 and value != 11:
            self.explanation.setText("<small>A tie for %dst place will be settled by tiebreak arrows. All other ties will be settled by drawing lots." % value)
        elif value % 10 == 2 and value != 12:
            self.explanation.setText("<small>A tie for %dnd place will be settled by tiebreak arrows. All other ties will be settled by drawing lots." % value)
        elif value % 10 == 3 and value != 13:
            self.explanation.setText("<small>A tie for %drd place will be settled by tiebreak arrows. All other ties will be settled by drawing lots." % value)
        else:
            self.explanation.setText("<small>A tie for %dth place will be settled by tiebreak arrows. All other ties will be settled by drawing lots." % value)
        self.options["cutoff"] = value
        self.optionsChanged.emit(self.options)
