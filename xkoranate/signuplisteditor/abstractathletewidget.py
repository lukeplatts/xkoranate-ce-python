import uuid

from PySide6.QtCore import Qt, Signal

from ..abstracttreewidget import XkorAbstractTreeWidget
from ..rng import Mt19937


def _uuidToString(u):
    if u is None:  # null QUuid
        return "{00000000-0000-0000-0000-000000000000}"
    return "{%s}" % u


def _uuidFromString(s):
    try:
        u = uuid.UUID(str(s).strip("{}"))
    except (AttributeError, TypeError, ValueError):
        return None
    return None if u.int == 0 else u


def _indexOf(l, value):
    # QStringList::indexOf semantics
    try:
        return l.index(value)
    except ValueError:
        return -1


class XkorAbstractAthleteWidget(XkorAbstractTreeWidget):
    itemDeleted = Signal(object)  # QUuid
    signupListDirectoryChanged = Signal(str)

    def __init__(self, columnKeys, columnNames, columnTypes, minDouble, maxDouble, doubleStep):
        self.r = Mt19937()  # std::tr1::mt19937 member
        super().__init__()
        self.m_columnKeys = list(columnKeys)
        self.m_columnNames = list(columnNames)
        self.m_columnTypes = list(columnTypes)
        self.m_minDouble = minDouble
        self.m_maxDouble = maxDouble
        self.m_doubleStep = doubleStep

    def initItem(self, item, athleteName="", id=None, nation="", skill=0, properties=None):
        # C++ overloads: the no-argument form generates a fresh random ID
        raise NotImplementedError  # pure virtual

    def deleteItems(self):
        selection = self.treeWidget.selectedItems()
        for i in selection:
            self.itemDeleted.emit(_uuidFromString(i.data(_indexOf(self.m_columnKeys, "name"), Qt.UserRole)))
        XkorAbstractTreeWidget.deleteItems(self)

    def athletes(self):
        raise NotImplementedError  # pure virtual

    def setAthletes(self, athletes):
        raise NotImplementedError  # pure virtual

    def setMaxRank(self, newMax):
        raise NotImplementedError  # pure virtual

    def setMinRank(self, newMin):
        raise NotImplementedError  # pure virtual
