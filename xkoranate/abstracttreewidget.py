from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QAbstractItemView, QGridLayout, QStyle,
                               QToolBar, QTreeWidgetItem, QWidget)

from .icons import icon
from .treewidget import XkorTreeWidget


class XkorAbstractTreeWidget(QWidget):
    listChanged = Signal()

    def __init__(self):
        super().__init__()
        self.isInUse = True
        self.treeWidget = XkorTreeWidget()
        self.treeWidget.setRootIsDecorated(False)
        self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setEditTriggers(QAbstractItemView.DoubleClicked
                                        | QAbstractItemView.SelectedClicked
                                        | QAbstractItemView.EditKeyPressed)
        # disable Delete if there is no selection, et cetera
        self.treeWidget.itemSelectionChanged.connect(self.updateButtons)
        # if we change the list, we need to tell the table generator
        self.treeWidget.itemChanged.connect(self.listIsEdited)

        self.insertAction = QAction(icon("add"), self.insertionText(), self)
        self.insertAction.setEnabled(True)
        self.insertAction.triggered.connect(self.insertItem)

        self.deleteAction = QAction(icon("remove"), self.deletionText(), self)
        self.deleteAction.setEnabled(False)
        self.deleteAction.triggered.connect(self.deleteItems)

        self.moveUpAction = QAction(self.movingUpText(), self)
        self.moveUpAction.setEnabled(False)
        self.moveUpAction.triggered.connect(self.moveUp)

        self.moveDownAction = QAction(self.movingDownText(), self)
        self.moveDownAction.setEnabled(False)
        self.moveDownAction.triggered.connect(self.moveDown)

        self.listChanged.connect(self.updateButtons)
        self.isInUse = False

    def initItem(self, item):
        pass

    def insertionText(self):
        return "Add item"

    def deletionText(self):
        return "Remove items"

    def movingUpText(self):
        return "Move item up"

    def movingDownText(self):
        return "Move item down"

    def createItem(self):
        item = QTreeWidgetItem(self.treeWidget)
        self.treeWidget.setCurrentItem(item, 0)
        item.setFlags((item.flags() | Qt.ItemIsEditable) & ~Qt.ItemIsDropEnabled)
        return item

    def clear(self):
        self.treeWidget.clear()
        self.listChanged.emit()

    def deleteItems(self):
        self.isInUse = True
        selection = self.treeWidget.selectedItems()
        for i in selection:
            parent = i.parent()
            if parent:
                parent.takeChild(parent.indexOfChild(i))
            else:
                self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(i))
        self.isInUse = False
        self.listChanged.emit()

    def insertItem(self):
        self.isInUse = True
        item = self.createItem()
        self.initItem(item)
        self.treeWidget.editItem(item, 0)
        self.isInUse = False
        self.listChanged.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up and event.modifiers() & Qt.ControlModifier:
            self.moveUpAction.trigger()
        elif event.key() == Qt.Key_Down and event.modifiers() & Qt.ControlModifier:
            self.moveDownAction.trigger()

    def listIsEdited(self):
        if not self.isInUse:
            self.listChanged.emit()

    def moveDown(self):
        self.isInUse = True
        selection = self.treeWidget.selectedItems()
        item = selection[0]
        parent = item.parent()
        if parent and parent.indexOfChild(item) < parent.childCount() - 1:
            index = parent.indexOfChild(item)
            parent.takeChild(index)
            parent.insertChild(index + 1, item)
            self.treeWidget.setCurrentItem(item, 0)
        elif self.treeWidget.indexOfTopLevelItem(item) < self.treeWidget.topLevelItemCount() - 1:
            index = self.treeWidget.indexOfTopLevelItem(item)
            self.treeWidget.takeTopLevelItem(index)
            self.treeWidget.insertTopLevelItem(index + 1, item)
            self.treeWidget.setCurrentItem(item, 0)
        self.treeWidget.setExpanded(self.treeWidget.currentIndex(), True)
        self.isInUse = False
        self.listChanged.emit()

    def moveUp(self):
        self.isInUse = True
        selection = self.treeWidget.selectedItems()
        item = selection[0]
        parent = item.parent()
        if parent and parent.indexOfChild(item) > 0:
            index = parent.indexOfChild(item)
            parent.takeChild(index)
            parent.insertChild(index - 1, item)
            self.treeWidget.setCurrentItem(item, 0)
        elif self.treeWidget.indexOfTopLevelItem(item) > 0:
            index = self.treeWidget.indexOfTopLevelItem(item)
            self.treeWidget.takeTopLevelItem(index)
            self.treeWidget.insertTopLevelItem(index - 1, item)
            self.treeWidget.setCurrentItem(item, 0)
        self.treeWidget.setExpanded(self.treeWidget.currentIndex(), True)
        self.isInUse = False
        self.listChanged.emit()

    def setupLayout(self, actions, isVertical=False):
        # tool bar
        toolBar = QToolBar()
        small = self.style().pixelMetric(QStyle.PM_SmallIconSize)
        toolBar.setIconSize(QSize(small, small))
        if isVertical:
            toolBar.setOrientation(Qt.Vertical)
        for i in actions:
            if i is None:
                toolBar.addSeparator()
            else:
                toolBar.addAction(i)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.treeWidget, 0, 0)
        if isVertical:
            self.layout.addWidget(toolBar, 0, 1, Qt.AlignCenter)
        else:
            self.layout.addWidget(toolBar, 1, 0, Qt.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def updateButtons(self):
        selection = self.treeWidget.selectedItems()
        self.deleteAction.setEnabled(len(selection) > 0)

        if len(selection) == 1:
            # can only move up/down if we're not at the top/bottom
            item = selection[0]
            parent = item.parent()
            canMoveUp = canMoveDown = True
            if parent:
                index = parent.indexOfChild(item)
                if index == 0:  # top
                    canMoveUp = False
                if index == parent.childCount() - 1:  # bottom
                    canMoveDown = False
            else:
                index = self.treeWidget.indexOfTopLevelItem(item)
                if index == 0:  # top
                    canMoveUp = False
                if index == self.treeWidget.topLevelItemCount() - 1:  # bottom
                    canMoveDown = False
            self.moveUpAction.setEnabled(canMoveUp)
            self.moveDownAction.setEnabled(canMoveDown)
        else:
            # can't manipulate athletes if more than one is selected
            self.moveUpAction.setEnabled(False)
            self.moveDownAction.setEnabled(False)
