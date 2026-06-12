from PySide6.QtCore import QDir, QFileInfo, QSettings, Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QApplication, QToolBar

from .centralwidget import XkorCentralWidget
from .icons import icon
from .mainwindow import XkorMainWindow
from .paths import sportsDir
from .variant import toStringList


class XkorApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.tg = None
        self.modified = False

        self.settings = QSettings("thirdgeek.com", "xkoranate")

        self.setDefaultSettings()  # in case we haven’t run the application before

        self.mainWindow = XkorMainWindow()
        if hasattr(self.mainWindow, "setUnifiedTitleAndToolBarOnMac"):
            self.mainWindow.setUnifiedTitleAndToolBarOnMac(True)

        self.cw = XkorCentralWidget()
        self.cw.eventDirectoryChanged.connect(self.setEventDirectory)
        self.cw.fileChanged.connect(self.setFileName)
        self.cw.fileEdited.connect(self.setModified)
        self.cw.resultExportDirectoryChanged.connect(self.setResultExportDirectory)
        self.cw.signupListDirectoryChanged.connect(self.setSignupListDirectory)

        # set up actions
        self.newAction = QAction(icon("document-new"), "New file…", self)
        self.newAction.setShortcut(QKeySequence(QKeySequence.New))
        self.newAction.triggered.connect(lambda: self.cw.newFile())

        self.openAction = QAction(icon("document-open"), "Open file…", self)
        self.openAction.setShortcut(QKeySequence(QKeySequence.Open))
        self.openAction.triggered.connect(lambda: self.cw.openFile())

        self.saveAction = QAction(icon("document-save"), "Save file…", self)
        self.saveAction.setShortcut(QKeySequence(QKeySequence.Save))
        self.saveAction.triggered.connect(lambda: self.cw.saveFile())

        self.saveAsAction = QAction(icon("document-save-as"), "Save file as…", self)
        self.saveAsAction.setShortcut(QKeySequence(Qt.CTRL | Qt.SHIFT | Qt.Key_S))
        self.saveAsAction.triggered.connect(lambda: self.cw.saveFileAs())

        self.tableAction = QAction(icon("table-generator"), "Table generator", self)
        self.tableAction.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_T))
        self.tableAction.triggered.connect(self.tableGenerator)

        # toolbar
        self.toolBar = QToolBar()
        self.toolBar.setMovable(False)
        self.toolBar.addAction(self.newAction)
        self.toolBar.addAction(self.openAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.saveAction)
        self.toolBar.addAction(self.saveAsAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.tableAction)

        self.mainWindow.setCentralWidget(self.cw)
        self.mainWindow.addToolBar(self.toolBar)
        self.mainWindow.setWindowTitle("untitled[*] – xkoranate")

        # C++ only did this on X11; on macOS the .app bundle provides the dock
        # icon, so setting it unconditionally is harmless
        self.mainWindow.setWindowIcon(icon("xkoranate"))

        self.mainWindow.show()

    def loadSports(self):
        self.refreshSearchPaths()
        self.cw.loadSports()

    # bool notify(QObject *, QEvent *) is not ported: Python exceptions
    # propagate fine without it

    def refreshSearchPaths(self):
        QDir.setSearchPaths("sports", [sportsDir()])

        QDir.setSearchPaths("events", toStringList(self.settings.value("eventDirectory")))
        QDir.setSearchPaths("resultsExport", toStringList(self.settings.value("resultExportDirectory")))
        QDir.setSearchPaths("resultsImport", toStringList(self.settings.value("resultImportDirectory")))
        QDir.setSearchPaths("signupLists", toStringList(self.settings.value("signupListDirectory")))
        QDir.setSearchPaths("tables", toStringList(self.settings.value("tableDirectory")))

    def setDefaultSettings(self):
        if not self.settings.contains("eventDirectory"):
            self.setEventDirectory(QDir.homePath())
        if not self.settings.contains("resultExportDirectory"):
            self.setResultExportDirectory(QDir.homePath())
        if not self.settings.contains("resultImportDirectory"):
            self.setResultImportDirectory(QDir.homePath())
        if not self.settings.contains("signupListDirectory"):
            self.setSignupListDirectory(QDir.homePath())
        if not self.settings.contains("tableDirectory"):
            self.setTableDirectory(QDir.homePath())

    def setEventDirectory(self, dir):
        self.settings.setValue("eventDirectory", dir)
        self.refreshSearchPaths()

    def setFileName(self, filename):
        displayName = "untitled"
        if filename != "":
            displayName = QFileInfo(filename).fileName()
        self.mainWindow.setWindowTitle(displayName + "[*] – xkoranate")
        self.setModified(False)

    def setModified(self, newModified=True):
        self.modified = newModified
        self.mainWindow.setWindowModified(newModified)

    def setResultExportDirectory(self, dir):
        self.settings.setValue("resultExportDirectory", dir)
        self.refreshSearchPaths()

    def setResultImportDirectory(self, dir):
        self.settings.setValue("resultImportDirectory", dir)
        self.refreshSearchPaths()

    def setSignupListDirectory(self, dir):
        self.settings.setValue("signupListDirectory", dir)
        self.refreshSearchPaths()

    def setTableDirectory(self, dir):
        self.settings.setValue("tableDirectory", dir)
        self.refreshSearchPaths()

    def tableGenerator(self):
        from .tablegenerator.tablegeneratorwindow import XkorTableGeneratorWindow

        if self.tg is not None:  # delete tg
            self.tg.close()
            self.tg.deleteLater()
        self.tg = XkorTableGeneratorWindow()
        self.tg.resultImportDirectoryChanged.connect(self.setResultImportDirectory)
        self.tg.tableDirectoryChanged.connect(self.setTableDirectory)
        self.tg.show()
