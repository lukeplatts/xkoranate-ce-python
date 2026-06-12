"""Replacement for the Qt resource file icons.qrc: icon("document-new") etc."""

import os

from PySide6.QtGui import QIcon

from .paths import iconsDir


def icon(name):
    return QIcon(os.path.join(iconsDir(), name + ".png"))
