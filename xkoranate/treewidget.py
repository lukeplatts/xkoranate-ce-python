from PySide6.QtWidgets import QAbstractItemView, QTreeWidget


class XkorTreeWidget(QTreeWidget):
    def moveCursor(self, cursorAction, modifiers):
        index = self.currentIndex()
        if cursorAction == QAbstractItemView.CursorAction.MoveNext:
            if index.column() < self.columnCount() - 1:
                return self.model().index(index.row(), index.column() + 1, index.parent())
        elif cursorAction == QAbstractItemView.CursorAction.MovePrevious:
            if index.column() > 0:
                return self.model().index(index.row(), index.column() - 1, index.parent())
        # in all other cases, let Qt do the hard work
        return QTreeWidget.moveCursor(self, cursorAction, modifiers)
