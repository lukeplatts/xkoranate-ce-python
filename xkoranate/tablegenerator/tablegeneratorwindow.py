from PySide6.QtCore import QFileInfo, Qt, Signal
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QToolBar

from ..icons import icon
from .tablegenerator import XkorTableGenerator


class XkorTableGeneratorWindow(QMainWindow):
    resultImportDirectoryChanged = Signal(str)
    tableDirectoryChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("untitled – xkoranate table generator")

        self.generator = XkorTableGenerator()
        self.setCentralWidget(self.generator)
        self.generator.fileChanged.connect(self.setFileName)
        self.generator.fileEdited.connect(self.setModified)
        self.generator.resultImportDirectoryChanged.connect(self.setResultImportDirectory)
        self.generator.tableDirectoryChanged.connect(self.setTableDirectory)

        self.newAction = QAction(icon("document-new"), "New file", self)
        self.newAction.setShortcut(QKeySequence.New)
        self.newAction.triggered.connect(lambda: self.generator.reset())

        self.openAction = QAction(icon("document-open"), "Open file…", self)
        self.openAction.setShortcut(QKeySequence.Open)
        self.openAction.triggered.connect(lambda: self.generator.openFile())

        self.saveAction = QAction(icon("document-save"), "Save file", self)
        self.saveAction.setShortcut(QKeySequence.Save)
        self.saveAction.triggered.connect(lambda: self.generator.saveFile())

        self.saveAsAction = QAction(icon("document-save-as"), "Save file as…", self)
        self.saveAsAction.setShortcut(QKeySequence.SaveAs)
        self.saveAsAction.triggered.connect(lambda: self.generator.saveFileAs())

        self.importAction = QAction(icon("document-import"), "Import match results…", self)
        self.importAction.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_I))
        self.importAction.triggered.connect(lambda: self.generator.importResults())

        self.generateAction = QAction(icon("table-generator-refresh"), "Generate table", self)
        self.generateAction.setShortcut(QKeySequence.Refresh)
        self.generateAction.triggered.connect(lambda: self.generator.generateTable())

        self.toolBar = QToolBar()
        self.toolBar.setMovable(False)
        self.toolBar.addAction(self.newAction)
        self.toolBar.addAction(self.openAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.saveAction)
        self.toolBar.addAction(self.saveAsAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.importAction)
        self.toolBar.addAction(self.generateAction)

        self.addToolBar(self.toolBar)
        self.setUnifiedTitleAndToolBarOnMac(True)

    def closeEvent(self, event):
        if self.generator.close():
            QMainWindow.closeEvent(self, event)
        else:
            event.ignore()

    def setFileName(self, filename):
        displayName = "untitled"
        if filename != "":
            displayName = QFileInfo(filename).fileName()
        self.setWindowTitle(displayName + "[*] – xkoranate table generator")
        self.setModified(False)

    def setModified(self, newModified=True):
        self.setWindowModified(newModified)

    def setResultImportDirectory(self, dir):
        self.resultImportDirectoryChanged.emit(dir)

    def setTableDirectory(self, dir):
        self.tableDirectoryChanged.emit(dir)
