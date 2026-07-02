from PySide6.QtCore import QDir, QFileInfo, QSettings, Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
                               QToolBar, QWidget)

from .centralwidget import XkorCentralWidget
from .icons import icon, icon_action
from .mainwindow import XkorMainWindow
from .paths import sportsDir
from . import theme
from .ui.toggleswitch import XkorToggleSwitch
from .variant import toStringList


class XkorApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        # flat light/dark theme — must be applied before any widgets are
        # constructed so themed palettes/metrics are in place from the start
        theme.apply(self)

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
        self.newAction = icon_action("document-new", "New file…", self)
        self.newAction.setShortcut(QKeySequence(QKeySequence.New))
        self.newAction.triggered.connect(lambda: self.cw.newFile())

        self.openAction = icon_action("document-open", "Open file…", self)
        self.openAction.setShortcut(QKeySequence(QKeySequence.Open))
        self.openAction.triggered.connect(lambda: self.cw.openFile())

        self.saveAction = icon_action("document-save", "Save file…", self)
        self.saveAction.setShortcut(QKeySequence(QKeySequence.Save))
        self.saveAction.triggered.connect(lambda: self.cw.saveFile())

        self.saveAsAction = icon_action("document-save-as", "Save file as…", self)
        self.saveAsAction.setShortcut(QKeySequence(Qt.CTRL | Qt.SHIFT | Qt.Key_S))
        self.saveAsAction.triggered.connect(lambda: self.cw.saveFileAs())

        self.tableAction = icon_action("table-generator", "Table generator", self)
        self.tableAction.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_T))
        self.tableAction.triggered.connect(self.tableGenerator)

        self.quitAction = QAction("Quit", self)
        self.quitAction.setShortcut(QKeySequence(QKeySequence.Quit))
        self.quitAction.triggered.connect(self.closeAllWindows)

        self.darkModeAction = QAction("Dark mode", self)
        self.darkModeAction.setCheckable(True)
        self.darkModeAction.setChecked(theme.is_dark())
        self.darkModeAction.setShortcut(QKeySequence(Qt.CTRL | Qt.SHIFT | Qt.Key_D))
        self.darkModeAction.toggled.connect(self.setThemeDark)

        # menu bar — the standard cross-platform place shortcuts are
        # discoverable; the toolbar's icons/tooltips don't show them
        menuBar = self.mainWindow.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.tableAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.quitAction)

        viewMenu = menuBar.addMenu("&View")
        viewMenu.addAction(self.darkModeAction)

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

        # push the theme switch to the far right of the toolbar
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolBar.addWidget(spacer)

        themeBox = QWidget()
        themeRow = QHBoxLayout(themeBox)
        themeRow.setContentsMargins(0, 0, 8, 0)
        themeRow.setSpacing(6)
        themeRow.addWidget(QLabel("Dark mode"))
        self.themeSwitch = XkorToggleSwitch()
        self.themeSwitch.setChecked(theme.is_dark())
        self.themeSwitch.setToolTip("Switch between light and dark mode")
        self.themeSwitch.toggled.connect(self.setThemeDark)
        # keep the toolbar switch and the View menu's checkbox in lockstep
        self.themeSwitch.toggled.connect(self.darkModeAction.setChecked)
        self.darkModeAction.toggled.connect(self.themeSwitch.setChecked)
        themeRow.addWidget(self.themeSwitch)
        self.toolBar.addWidget(themeBox)

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

    def setThemeDark(self, dark):
        theme.set_mode(self, "dark" if dark else "light")

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
