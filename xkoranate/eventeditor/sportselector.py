import sys

from PySide6.QtCore import QItemSelectionModel, QModelIndex, Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGridLayout, QLabel, QTreeView, QWidget

from ..exceptions import XkorFileNotFoundException
from ..sport import XkorSport
from .sportmodel import SPORT_DATA, SPORT_NAME, XkorSportModel


class XkorSportSelector(QWidget):
    paradigmOptionsChanged = Signal(dict)
    sportChanged = Signal(object)  # XkorSport

    def __init__(self, parent=None):
        super().__init__(parent)
        self.paradigmOptionsWidget = None
        self.selectionModel = None
        self.isLoading = False
        self.currentParadigmOptions = {}
        self._model = None  # keep a Python reference to the view's model

        self.sportView = QTreeView()
        self.sportView.setHeaderHidden(True)

        headingFont = QFont()
        headingFont.setWeight(QFont.Bold)

        self.layout = QGridLayout(self)
        label = QLabel("Select sport")
        label.setFont(headingFont)
        self.layout.addWidget(label, 0, 0, Qt.AlignCenter)
        self.layout.addWidget(self.sportView, 1, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def setParadigmOptions(self, paradigmOptions):
        self.currentParadigmOptions = paradigmOptions
        if self.paradigmOptionsWidget:
            self.paradigmOptionsWidget.setOptions(paradigmOptions)

    def setSelectedSport(self, fullNameOrIndex):
        # C++ overloads: setSelectedSport(QString) and setSelectedSport(QModelIndex)
        if isinstance(fullNameOrIndex, QModelIndex):
            index = fullNameOrIndex
        else:
            index = self.sportView.model().findSport(fullNameOrIndex)

        if index.isValid():
            self.sportView.scrollTo(index)
            self.selectionModel.select(index, QItemSelectionModel.ClearAndSelect)
            if index.parent() != QModelIndex():
                self.sportView.setExpanded(index.parent(), True)
                if index.parent().parent() != QModelIndex():
                    self.sportView.setExpanded(index.parent().parent(), True)
        else:
            self.sportView.clearSelection()
        self.updateSport()

    def sport(self):
        rval = XkorSport()
        if self.selectionModel:
            l = self.selectionModel.selectedRows()
            for i in l:
                if i.data(SPORT_NAME) is not None:
                    rval = i.data(SPORT_DATA)
        else:
            rval = XkorSport()
        return rval

    def updateParadigmOptions(self, paradigmOptions):
        self.currentParadigmOptions = paradigmOptions
        self.paradigmOptionsChanged.emit(paradigmOptions)

    def updateSport(self):
        s = self.sport()
        if not self.isLoading:
            self.sportChanged.emit(s)

        if self.paradigmOptionsWidget:
            self.layout.removeWidget(self.paradigmOptionsWidget)
            self.paradigmOptionsWidget.setParent(None)
            self.paradigmOptionsWidget.deleteLater()
        self.paradigmOptionsWidget = None

        # check whether the paradigm has an options dialog
        from ..paradigms.paradigmfactory import XkorParadigmFactory

        p = XkorParadigmFactory.newParadigm(s.paradigm())

        if s.name() != "" and p.hasOptionsWidget():
            self.paradigmOptionsWidget = p.newOptionsWidget(self.currentParadigmOptions)
            self.layout.addWidget(self.paradigmOptionsWidget)
            self.paradigmOptionsWidget.show()
            self.paradigmOptionsWidget.optionsChanged.connect(self.updateParadigmOptions)

    def updateSportList(self):
        self.isLoading = True
        try:
            sportName = self.sport().name()

            # create a model
            model = XkorSportModel()
            self.sportView.setModel(model)
            self._model = model

            self.selectionModel = QItemSelectionModel(model)
            self.sportView.setSelectionModel(self.selectionModel)
            self.selectionModel.selectionChanged.connect(self.updateSport)

            # load the sports
            from ..xml.xmlindex import XkorXmlIndex
            from ..xml.xmlsportreader import XkorXmlSportReader

            x = XkorXmlIndex()
            x.traverse("sports:./")

            s = x.getAllFiles()
            for key in sorted(s):  # std::map iterates in sorted-key order
                r = XkorXmlSportReader(s[key])
                model.insertSport(r.sport())
            self.sportView.reset()

            self.setSelectedSport(sportName)
        except XkorFileNotFoundException as ex:
            print("caught XkorFileNotFoundException in XkorSportSelector::updateSportList for",
                  ex.fileType(), " file ", ex.fileName(), file=sys.stderr)
        self.isLoading = False
