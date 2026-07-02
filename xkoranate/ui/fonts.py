"""Small font helpers, so the app's few font decisions live in one place."""

from PySide6.QtGui import QFont


def monospace_font():
    """A monospace font for fixed-width results/match output."""
    hint = QFont()
    hint.setStyleHint(QFont.TypeWriter)
    return QFont(hint.defaultFamily())


def column_width_for(widget, sampleText, padding=28):
    """A tree/table column width sized to fit sampleText in widget's current
    font, plus padding for the sort indicator, instead of a hardcoded pixel
    value that stays put (and can start truncating) if the font gets bigger."""
    return widget.fontMetrics().horizontalAdvance(sampleText) + padding
