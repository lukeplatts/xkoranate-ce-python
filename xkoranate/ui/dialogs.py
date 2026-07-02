"""Shared QMessageBox construction. Several screens pop an "xkoranate"-branded
confirmation dialog (unsaved changes, destructive re-scorination, etc.); this
gives them one place to build it consistently instead of each hand-rolling
the brand icon pixmap and modality flags."""

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox, QStyle

from .. import theme
from ..paths import iconsDir


def brand_pixmap(widget, size=None):
    """The xkoranate icon, scaled for use as a QMessageBox.setIconPixmap()."""
    iconSize = size or widget.style().pixelMetric(QStyle.PM_MessageBoxIconSize)
    return (QPixmap(os.path.join(iconsDir(), "xkoranate.png"))
            .scaled(iconSize, iconSize, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))


def message_box(parent, text, buttons, informativeText="", icon=QMessageBox.NoIcon,
                defaultButton=None, escapeButton=None, destructiveButton=None):
    """Build (but don't exec()) an "xkoranate"-branded QMessageBox. Passing
    icon=QMessageBox.NoIcon (the default) uses the brand icon in place of a
    generic system one; pass e.g. QMessageBox.Warning to get that instead.

    destructiveButton names the button (e.g. QMessageBox.Discard, or Ok when
    "Ok" means "yes, lose my data") that should read as a warning rather than
    the app's positive accent colour — so "discard my changes" never looks
    like the safe, recommended choice. Cancel/Close, if present, are recoloured
    to a neutral grey for the same reason: backing out isn't the accent action
    either."""
    box = QMessageBox(icon, "xkoranate", text, buttons, parent)
    if icon == QMessageBox.NoIcon:
        box.setIconPixmap(brand_pixmap(parent))
    if informativeText:
        box.setInformativeText(informativeText)
    if defaultButton is not None:
        box.setDefaultButton(defaultButton)
    if escapeButton is not None:
        box.setEscapeButton(escapeButton)
    box.setWindowModality(Qt.WindowModal)

    dangerBtn = box.button(destructiveButton) if destructiveButton is not None else None
    if dangerBtn is not None:
        dangerBtn.setStyleSheet(
            "QPushButton { color: %s; border-color: %s; }" % (theme.danger(), theme.danger()))

    for role in (QMessageBox.Cancel, QMessageBox.Close):
        neutralBtn = box.button(role)
        if neutralBtn is not None and neutralBtn is not dangerBtn:
            # qdarktheme fills whichever button is QMessageBox.setDefaultButton()
            # with the accent colour (its QPushButton:default rule) — override
            # background/border too, not just text colour, so a
            # defaultButton=Cancel/Close never reads as the accent action
            neutralBtn.setStyleSheet(
                "QPushButton { background: transparent; border: 1px solid %s; color: %s; }"
                % (theme.muted(), theme.muted()))

    return box
