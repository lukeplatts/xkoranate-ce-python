"""Small typography helper for a consistent heading scale.

Replaces the ad-hoc ``QFont(); setWeight(Bold)`` blocks duplicated across the
editor screens with one place that defines the type scale.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel

from .. import theme

# level -> (point-size multiplier over the base font, weight)
_SCALE = {
    1: (1.5, QFont.DemiBold),   # screen / page title
    2: (1.25, QFont.DemiBold),  # section heading
    3: (1.0, QFont.DemiBold),   # emphasised label (e.g. nav categories)
}


def apply_heading(label, level=1, accent=False):
    """Style an existing label as a heading at the given level."""
    mult, weight = _SCALE.get(level, _SCALE[1])
    font = label.font()
    base = font.pointSizeF() if font.pointSizeF() > 0 else 13.0
    font.setPointSizeF(base * mult)
    font.setWeight(weight)
    label.setFont(font)
    if accent:
        label.setStyleSheet("color: %s;" % theme.accent_text())
    return label


def heading_label(text, level=1, center=False, accent=False):
    """Create a styled heading QLabel."""
    label = QLabel(text)
    apply_heading(label, level, accent)
    if center:
        label.setAlignment(Qt.AlignCenter)
    return label
