# PyInstaller spec for the xkoranate-CE macOS app bundle.
# Build with: .venv/bin/pyinstaller --noconfirm xkoranate.spec

a = Analysis(
    ["launcher.py"],
    pathex=[],
    datas=[
        ("sports", "sports"),
        ("xkoranate/icons", "xkoranate/icons"),
    ],
    hiddenimports=[],
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
        "PySide6.QtOpenGL", "PySide6.QtOpenGLWidgets", "PySide6.QtSvg",
        "PySide6.QtSvgWidgets", "PySide6.QtUiTools", "PySide6.QtXml",
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="xkoranate",
)

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
        # the original xkoranate UI is light-themed; opt out of dark mode
        "NSRequiresAquaSystemAppearance": True,
    },
)
