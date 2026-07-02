"""Small font helpers, so the app's few font decisions live in one place."""

from PySide6.QtGui import QFont


def monospace_font():
    """A monospace font for fixed-width results/match output. Courier New,
    matching the font forum.nationstates.net uses for its [pre] blocks."""
    font = QFont("Courier New")
    font.setStyleHint(QFont.TypeWriter)
    return font


def column_width_for(widget, sampleText, padding=28):
    """A tree/table column width sized to fit sampleText in widget's current
    font, plus padding for the sort indicator, instead of a hardcoded pixel
    value that stays put (and can start truncating) if the font gets bigger."""
    return widget.fontMetrics().horizontalAdvance(sampleText) + padding


def widen_combo_popup(combo):
    """On macOS, a QComboBox's popup list renders with a smaller font than
    the closed box itself (a Cocoa style quirk that survives even an explicit
    view().setFont() override), so the popup can come out narrower than the
    text it's displaying and clip it. Call after (re)populating combo's items
    to force the popup to be at least as wide as the box, which is always
    wide enough for every item since the box's own AdjustToContents sizeHint
    is measured with the box's (larger) font."""
    combo.view().setMinimumWidth(combo.sizeHint().width())
