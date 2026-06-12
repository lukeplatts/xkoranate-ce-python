from PySide6.QtWidgets import QMainWindow


class XkorMainWindow(QMainWindow):
    def closeEvent(self, event):
        if self.centralWidget().close():
            QMainWindow.closeEvent(self, event)
        else:
            event.ignore()
