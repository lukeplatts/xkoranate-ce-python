import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication

from xkoranate.application import XkorApplication


def main():
    # Qt6 already scales for whole-number HiDPI factors by default; on a
    # fractional scale (e.g. Windows' 125%/150%) PassThrough keeps text and
    # icons crisp instead of Qt rounding to the nearest integer factor first.
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = XkorApplication(sys.argv)
    app.loadSports()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
