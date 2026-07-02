from PySide6.QtWidgets import QSplitter


class XkorThinSplitter(QSplitter):
    """A splitter with a slim handle. The handle is painted by the application
    theme rather than by hand (the original drew its own divider line)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHandleWidth(1)
