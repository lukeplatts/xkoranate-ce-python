"""Central place for the application's visual theme.

A modern light Material theme is applied once at startup via qt-material. The
accent/ink colours defined here are reused by the icon loader (icons.py) and the
typography helper (ui/typography.py) so the look stays consistent.
"""

# Material "light_blue" primary, used for headings/accents and the active
# wizard step. Kept in sync with the qt-material theme below.
ACCENT = "#0277bd"      # primary (light blue 800)
INK = "#37474f"         # toolbar/glyph colour on a light surface (blue grey 800)
MUTED = "#78909c"       # secondary text (blue grey 400)

_THEME_XML = "light_blue.xml"


def apply(app):
    """Apply the light Material theme to the QApplication. Safe no-op if the
    theming library is unavailable (the app still runs with the native style)."""
    try:
        from qt_material import apply_stylesheet
    except Exception:
        return
    extra = {
        # tighten Material's default density a touch for a desktop tool
        "density_scale": "-1",
    }
    apply_stylesheet(app, theme=_THEME_XML, invert_secondary=True, extra=extra)
