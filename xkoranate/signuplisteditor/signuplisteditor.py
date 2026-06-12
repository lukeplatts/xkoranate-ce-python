from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QDoubleSpinBox, QFormLayout, QLabel,
                               QVBoxLayout, QWidget)

from ..signuplist import XkorSignupList


def _cloneSignupList(sl):
    # XkorSignupList is passed/returned by value in the C++
    rval = XkorSignupList()
    rval.ath = [a.clone() for a in sl.ath]
    rval.min = sl.min
    rval.max = sl.max
    return rval


class XkorSignupListEditor(QWidget):
    dataChanged = Signal()
    itemDeleted = Signal(object)  # QUuid
    signupListDirectoryChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isLoading = False

        self.athletes = None
        self.m_data = XkorSignupList()

        headingFont = QFont()
        headingFont.setWeight(QFont.Bold)
        label = QLabel("Set participants")
        label.setFont(headingFont)

        # minimum rank
        self.minRank = QDoubleSpinBox()
        self.minRank.setDecimals(3)
        self.minRank.setRange(-999.999, 1)
        self.minRank.valueChanged.connect(self.minRankChanged)

        # maximum rank
        self.maxRank = QDoubleSpinBox()
        self.maxRank.setValue(100)
        self.maxRank.setDecimals(3)
        self.maxRank.setRange(0, 9999.999)
        self.maxRank.valueChanged.connect(self.maxRankChanged)

        # form layout
        form = QFormLayout()
        form.addRow("Minimum skill:", self.minRank)
        form.addRow("Maximum skill:", self.maxRank)

        # layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(label, 0, Qt.AlignCenter)
        self.layout.addLayout(form, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.minRank.valueChanged.connect(self.setDataChanged)
        self.maxRank.valueChanged.connect(self.setDataChanged)

    def data(self):
        self.updateData()
        return _cloneSignupList(self.m_data)

    def maxRankChanged(self, newMax):
        # min rank can’t be higher than max rank
        self.minRank.setMaximum(newMax)

        # inform the athlete widget
        if self.athletes:
            self.athletes.setMaxRank(newMax)

    def minRankChanged(self, newMin):
        # max rank can’t be lower than min rank
        self.maxRank.setMinimum(newMin)

        # inform the athlete widget
        if self.athletes:
            self.athletes.setMinRank(newMin)

    def setData(self, data):
        data = _cloneSignupList(data)

        self.isLoading = True  # prevent dataChanged from being emitted

        self.minRank.setValue(data.minRank())
        self.maxRank.setValue(data.maxRank())
        if self.athletes:
            self.athletes.setMinRank(data.minRank())
            self.athletes.setMaxRank(data.maxRank())
            self.athletes.setAthletes(data.athletes())

        self.m_data = data
        self.isLoading = False  # allow dataChanged to be emitted if the user does stuff

    def setDataChanged(self):
        if not self.isLoading:
            self.dataChanged.emit()

    def setItemDeleted(self, id):
        self.itemDeleted.emit(id)

    def setSignupListDirectory(self, dir):
        self.signupListDirectoryChanged.emit(dir)

    def setSport(self, sport, paradigmOptions):
        self.updateData()

        if self.athletes:
            self.layout.removeWidget(self.athletes)
        if self.athletes is not None:  # delete athletes
            self.athletes.setParent(None)
            self.athletes.deleteLater()

        from ..paradigms.paradigmfactory import XkorParadigmFactory

        p = XkorParadigmFactory.newParadigmForSport(sport, paradigmOptions)

        self.athletes = p.newAthleteWidget()
        self.setData(self.m_data)
        self.layout.addWidget(self.athletes, 1)
        self.athletes.listChanged.connect(self.setDataChanged)
        self.athletes.itemDeleted.connect(self.setItemDeleted)
        self.athletes.signupListDirectoryChanged.connect(self.setSignupListDirectory)

    def updateData(self):
        self.m_data.setMinRank(self.minRank.value())
        self.m_data.setMaxRank(self.maxRank.value())
        if self.athletes:
            self.m_data.setAthletes(self.athletes.athletes())
