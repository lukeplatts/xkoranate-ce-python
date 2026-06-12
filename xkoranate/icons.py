"""Icon loader. Replaces the Qt resource file icons.qrc: icon("document-new").

Toolbar/action glyphs are served from the Material Design Icons font via
qtawesome, so the whole app gets a modern, theme-consistent icon set from the
single set of call sites that already use icon(<key>). Brand/raster images that
are not glyphs (the application icon) fall back to the bundled PNGs.
"""

import os

from PySide6.QtGui import QIcon

from .paths import iconsDir
from . import theme

# map the app's icon keys to Material Design Icon (mdi6) glyph names
_MDI = {
    "document-new": "mdi6.file-plus-outline",
    "document-open": "mdi6.folder-open-outline",
    "document-save": "mdi6.content-save-outline",
    "document-save-as": "mdi6.content-save-edit-outline",
    "document-import": "mdi6.import",
    "document-export": "mdi6.export",
    "table-generator": "mdi6.table",
    "table-generator-refresh": "mdi6.table-refresh",
    "add": "mdi6.plus",
    "remove": "mdi6.minus",
    "roll": "mdi6.dice-multiple-outline",
    "add-participant": "mdi6.account-plus-outline",
    "add-all-participants": "mdi6.account-multiple-plus-outline",
}


def _png(name):
    return QIcon(os.path.join(iconsDir(), name + ".png"))


def icon(name):
    glyph = _MDI.get(name)
    if glyph is not None:
        try:
            import qtawesome
            return qtawesome.icon(glyph, color=theme.INK)
        except Exception:
            pass  # fall back to a bundled PNG if qtawesome is unavailable
    return _png(name)
