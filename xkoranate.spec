# PyInstaller spec for the xkoranate-CE app — builds a macOS .app bundle,
# a Windows onedir exe, or a Linux onedir binary depending on the host OS.
# Build with: .venv/bin/pyinstaller --noconfirm xkoranate.spec

import sys

from PyInstaller.utils.hooks import collect_all

# qdarktheme (stylesheet templates + svg icons) and qtawesome (icon fonts +
# charmaps) load data files at runtime — collect them or the frozen app crashes
# at startup even though the dev run works.
_datas, _binaries, _hiddenimports = [], [], []
for _pkg in ("qdarktheme", "qtawesome"):
    d, b, h = collect_all(_pkg)
    _datas += d
    _binaries += b
    _hiddenimports += h

a = Analysis(
    ["launcher.py"],
    pathex=[],
    datas=[
        ("sports", "sports"),
        ("xkoranate/icons", "xkoranate/icons"),
    ] + _datas,
    binaries=_binaries,
    hiddenimports=_hiddenimports,
    excludes=[
        # trim Qt modules the app never uses to keep the bundle small
        "PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets", "PySide6.QtWebChannel",
        "PySide6.QtQml", "PySide6.QtQuick", "PySide6.QtQuickWidgets", "PySide6.QtQuick3D",
        "PySide6.QtMultimedia", "PySide6.QtMultimediaWidgets", "PySide6.QtCharts",
        "PySide6.QtDataVisualization", "PySide6.QtPdf", "PySide6.QtPdfWidgets",
        "PySide6.Qt3DCore", "PySide6.Qt3DRender", "PySide6.QtNetworkAuth",
        "PySide6.QtPositioning", "PySide6.QtLocation", "PySide6.QtBluetooth",
        "PySide6.QtSensors", "PySide6.QtSerialPort", "PySide6.QtSql",
        "PySide6.QtTest", "PySide6.QtDesigner", "PySide6.QtHelp",
        # NOTE: QtSvg/QtSvgWidgets are *not* excluded — qdarktheme's icon
        # engine imports PySide6.QtSvg internally at runtime (qt-material,
        # the previous theme dependency, didn't need it), so excluding them
        # crashes the frozen app on launch even though the dev run is fine.
        "PySide6.QtOpenGL", "PySide6.QtOpenGLWidgets",
        "PySide6.QtUiTools", "PySide6.QtXml",
        "PySide6.QtNetwork", "PySide6.QtDBus", "PySide6.QtConcurrent",
        "PySide6.QtPrintSupport", "PySide6.QtWebSockets", "PySide6.QtRemoteObjects",
        "PySide6.QtScxml", "PySide6.QtStateMachine", "PySide6.QtTextToSpeech",
        "PySide6.QtNfc", "PySide6.QtSpatialAudio", "PySide6.QtHttpServer",
        "PySide6.QtGraphs", "PySide6.QtGraphsWidgets",
        "tkinter",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="xkoranate",
    debug=False,
    strip=False,
    upx=False,
    console=False,
    icon="xkoranate/icons/xkoranate.ico" if sys.platform == "win32" else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="xkoranate",
)

# macOS gets a proper .app bundle; Windows/Linux ship as the onedir COLLECT
# output produced above (dist/xkoranate/xkoranate[.exe]).
if sys.platform == "darwin":
    app = BUNDLE(
        coll,
        name="xkoranate.app",
        icon="xkoranate/icons/xkoranate.icns",
        bundle_identifier="com.thirdgeek.xkoranate",
        info_plist={
            "CFBundleName": "xkoranate",
            "CFBundleDisplayName": "xkoranate",
            "CFBundleShortVersionString": "0.4.0",
            "NSHighResolutionCapable": True,
            # the app now ships its own light/dark toggle, so let macOS switch
            # window chrome (title bar) freely instead of forcing Aqua
            "NSRequiresAquaSystemAppearance": False,
        },
    )
