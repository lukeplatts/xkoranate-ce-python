import uuid

from PySide6.QtCore import QItemSelectionModel, QSize, Qt, Signal
from PySide6.QtWidgets import (QAbstractItemView, QGridLayout, QLabel, QStackedLayout,
                               QStyle, QToolBar, QTreeWidgetItem, QTreeWidgetItemIterator,
                               QWidget)

from ..abstracttreewidget import XkorAbstractTreeWidget
from ..ui.typography import heading_label
from .. import theme
from ..athlete import XkorAthlete
from ..exceptions import XkorSearchFailedException
from ..group import XkorGroup
from ..icons import icon_action
from ..rng import Mt19937
from ..signuplist import XkorSignupList
from .eventsetupdelegate import XkorEventSetupDelegate


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


def _cloneSignupList(sl):
    rval = XkorSignupList()
    rval.ath = [a.clone() for a in sl.ath]
    rval.min = sl.min
    rval.max = sl.max
    return rval


class XkorEventSetupWidget(XkorAbstractTreeWidget):
    slChanged = Signal()

    def __init__(self):
        super().__init__()
        self.availableAthleteNames = []  # mutated in place: shared with the delegate
        self.availableAthletes = []  # list of QUuid; shared with the delegate
        self.sl = XkorSignupList()
        self.r = Mt19937()  # backs std::random_shuffle in randomizeGroup

        self._delegate = XkorEventSetupDelegate(self.availableAthleteNames, self.availableAthletes)
        self.treeWidget.setItemDelegate(self._delegate)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setDragDropMode(QAbstractItemView.InternalMove)
        rootItem = self.treeWidget.invisibleRootItem()
        rootItem.setFlags(rootItem.flags() & ~Qt.ItemIsDropEnabled)

        # set up actions
        self.insertGroupAction = icon_action("add", "Create a group", self)
        self.insertGroupAction.triggered.connect(self.insertItem)

        self.insertAthleteAction = icon_action("add-participant", "Add a participant", self)
        self.insertAthleteAction.setEnabled(False)
        self.insertAthleteAction.triggered.connect(self.insertAthlete)

        self.insertAllAction = icon_action("add-all-participants", "Add all available participants", self)
        self.insertAllAction.setEnabled(False)
        self.insertAllAction.triggered.connect(self.insertAll)

        self.randomizeAction = icon_action("roll", "Randomize this group", self)
        self.randomizeAction.setEnabled(False)
        self.randomizeAction.triggered.connect(self.randomizeGroup)

        actions = [self.insertGroupAction, self.insertAthleteAction,
                   self.insertAllAction, self.deleteAction, self.randomizeAction]
        self.setupLayout(actions)

        self.slChanged.connect(self.updateAvailableAthletes)

    def insertionText(self):
        return "Create a group"

    def createAthlete(self, parent):
        item = QTreeWidgetItem(parent)
        self.treeWidget.setCurrentItem(item, 0)
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        return item

    def deleteAthlete(self, id):
        toDelete = []
        i = QTreeWidgetItemIterator(self.treeWidget)
        while i.value():
            item = i.value()
            # if this is an athlete, look up its ID
            if item.parent():
                if _uuidFromString(item.data(0, Qt.UserRole)) == id:
                    toDelete.append(item)
            i += 1
        for item in toDelete:
            parent = item.parent()
            parent.takeChild(parent.indexOfChild(item))
        self.listChanged.emit()

    def getAthleteByID(self, id):
        rval = XkorAthlete()
        try:
            rval = self.sl.getAthleteByID(id)
        except XkorSearchFailedException:
            pass

        if rval == XkorAthlete():
            err = "No athlete with ID "
            err += _uuidToString(id)
            err += " in XkorEventEditor::getAthleteBySN(QString)"
            raise XkorSearchFailedException(err)
        return rval

    def groups(self):
        rval = []
        for i in range(self.treeWidget.topLevelItemCount()):
            group = XkorGroup()
            group.name = self.treeWidget.topLevelItem(i).text(0)
            for j in range(self.treeWidget.topLevelItem(i).childCount()):
                group.athletes.append(_uuidFromString(self.treeWidget.topLevelItem(i).child(j).data(0, Qt.UserRole)))
            rval.append(group)
        return rval

    def initAthlete(self, athlete, id=None):
        # get the actual athlete so we can display its name
        try:
            a = self.getAthleteByID(id)
            athlete.setText(0, a.name + " (" + a.nation + ")")
        except XkorSearchFailedException:
            athlete.setText(0, "<unknown participant>")

        athlete.setFlags(athlete.flags() & ~Qt.ItemIsDropEnabled)
        athlete.setData(0, Qt.UserRole, _uuidToString(id))

    def initItem(self, group, groupName=""):  # initItem is used for groups
        group.setFlags((group.flags() | Qt.ItemIsDropEnabled) & ~Qt.ItemIsDragEnabled)
        group.setText(0, groupName)

    def insertAll(self):
        self.isInUse = True
        selection = self.treeWidget.selectedItems()
        parent = selection[0].parent()

        for i in range(len(self.availableAthletes)):
            self.initAthlete(self.createAthlete(parent if parent else selection[0]),
                             self.availableAthletes[i])
        self.isInUse = False
        self.listChanged.emit()

    def insertAthlete(self):
        self.isInUse = True
        selection = self.treeWidget.selectedItems()

        self.treeWidget.setCurrentItem(selection[0], 0, QItemSelectionModel.Clear)
        parent = selection[0].parent()

        athlete = self.createAthlete(parent if parent else selection[0])
        self.initAthlete(athlete)
        self.treeWidget.editItem(athlete, 0)
        self.isInUse = False
        self.listChanged.emit()

    def randomizeGroup(self):
        self.isInUse = True
        selection = self.treeWidget.selectedItems()

        # iterate in reverse so that the first group will be selected when we’re done
        for group in reversed(selection):
            if group.parent():
                group = group.parent()

            groupMembers = group.takeChildren()
            self.r.shuffle(groupMembers)  # std::random_shuffle
            group.addChildren(groupMembers)
            for j in groupMembers:
                self.treeWidget.setCurrentItem(j, 0, QItemSelectionModel.Select)
            self.treeWidget.setCurrentItem(group, 0, QItemSelectionModel.Select)
        self.isInUse = False
        self.listChanged.emit()

    def setGroups(self, g):
        self.isInUse = True
        for i in g:
            group = self.createItem()
            group.setExpanded(True)
            self.initItem(group, i.name)
            for j in i.athletes:
                athlete = self.createAthlete(group)
                self.initAthlete(athlete, j)
        self.isInUse = False
        self.listChanged.emit()

    def setSignupList(self, l):
        self.sl = _cloneSignupList(l)
        self.slChanged.emit()

    def setupLayout(self, actions):
        # label
        label = heading_label("Set up groups", level=1, center=True)

        # tool bar
        toolBar = QToolBar()
        small = self.style().pixelMetric(QStyle.PM_SmallIconSize)
        toolBar.setIconSize(QSize(small, small))
        for i in actions:
            if i is None:
                toolBar.addSeparator()
            else:
                toolBar.addAction(i)

        # empty-state hint, layered over the tree so a first-time user isn't
        # left staring at a blank rectangle
        self._emptyLabel = QLabel(self.emptyStateText())
        self._emptyLabel.setAlignment(Qt.AlignCenter)
        self._emptyLabel.setWordWrap(True)
        self._emptyLabel.setAttribute(Qt.WA_TransparentForMouseEvents)
        self._restyleEmptyLabel()
        theme.signal.changed.connect(self._restyleEmptyLabel)

        treeArea = QWidget()
        treeStack = QStackedLayout(treeArea)
        treeStack.setStackingMode(QStackedLayout.StackAll)
        treeStack.addWidget(self.treeWidget)
        treeStack.addWidget(self._emptyLabel)

        self.layout = QGridLayout(self)
        self.layout.addWidget(label, 0, 0, Qt.AlignCenter)
        self.layout.addWidget(treeArea, 1, 0)
        self.layout.addWidget(toolBar, 2, 0, Qt.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.updateEmptyState()

    def updateButtons(self):
        selection = self.treeWidget.selectedItems()

        self.deleteAction.setEnabled(len(selection) > 0)
        self.insertAthleteAction.setEnabled(len(self.availableAthletes) > 0)
        self.insertAllAction.setEnabled(len(self.availableAthletes) > 0)
        self.randomizeAction.setEnabled(len(selection) > 0)

        if len(selection) != 1:
            # can’t manipulate athletes if more than one is selected
            self.insertAthleteAction.setEnabled(False)
            self.insertAllAction.setEnabled(False)

    def updateAvailableAthletes(self):
        self.availableAthletes.clear()
        self.availableAthleteNames.clear()

        s = self.sl.athletes()
        for j in s:
            self.availableAthletes.append(j.id)
            self.availableAthleteNames.append(j.name + " (" + j.nation + ")")

        i = QTreeWidgetItemIterator(self.treeWidget)
        while i.value():
            item = i.value()
            # if this is an athlete, look up its ID
            if item.parent():
                try:
                    temp = self.getAthleteByID(_uuidFromString(item.data(0, Qt.UserRole)))
                    item.setText(0, temp.name + " (" + temp.nation + ")")
                except XkorSearchFailedException:
                    item.setText(0, "<unknown participant>")
            i += 1
        self.listChanged.emit()
