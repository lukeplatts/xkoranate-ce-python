# xkoranate-CE (Python port)

A faithful Python/PySide6 port of [xkoranate-CE](https://github.com/NS-Sports/Xkoranate-CE)
(xkoranate **C**ommunity **E**dition), the sports "scorinator" used by NS Sports,
the sports roleplay forum for NationStates. Originally written in Qt4/C++ by
Commerce Heights/ThirdGeek; this port preserves the original program's behavior —
scorination math, competition formats, file formats and UI — while running on
current macOS, Windows, and Linux via Python and Qt 6.

It simulates results for one hundred–plus disciplines across sixty-plus sports:
mass starts, head-to-head matches, round robins, multi-run events, shooting and
archery formats, and includes the league table generator.

The interface has a modern, light Material-style theme (via `qt-material`) with
Material Design Icons (`qtawesome`); the underlying behaviour is unchanged.

**Using the app?** See the [user guide](https://ns-sports.github.io/xkoranate-ce-python/)
for downloads, a tour of the event editor, and the table generator. The rest
of this README covers building and developing xkoranate itself.

## Running from source

```sh
python3 -m venv .venv
.venv/bin/pip install PySide6 qt-material qtawesome
.venv/bin/python -m xkoranate
```

## Building the app

The same PyInstaller spec (`xkoranate.spec`) produces a native build on
macOS, Windows, and Linux — it branches on the host platform automatically.

macOS/Linux:

```sh
.venv/bin/pip install pyinstaller
./build_app.sh
# macOS -> dist/xkoranate.app
# Linux -> dist/xkoranate/xkoranate
```

Windows:

```bat
.venv\Scripts\pip install pyinstaller
build_app.bat
:: -> dist\xkoranate\xkoranate.exe
```

The build bundles the `sports/` definitions directory alongside the app
(`Contents/Resources/sports/` on macOS, `sports/` next to the exe/binary on
Windows/Linux). Sport parameter files are plain XML and remain user-editable
there. The PyInstaller spec also bundles the `qdarktheme` and `qtawesome`
data files so the theme and icons work in the frozen app.

On Linux, PyInstaller only bundles a shared library into `dist/` if it can
resolve it (via `ldd`) on the *build* machine — anything missing there is
silently left out, and the resulting binary still builds fine but exits
instantly the moment anyone runs it, with no visible error. `.venv` needs the
full transitive dependency list installed before building for the shipped
binary to be self-contained (see the apt-get list in
`.github/workflows/release.yml`, which is CI-verified by launching the built
binary inside a bare container). The only two libraries that can't be
bundled this way are `libEGL`/`libGL` — Qt loads them via `dlopen` rather
than linking them, so PyInstaller can never detect or bundle them. They're
left to resolve from the host's graphics driver, which every real Linux
desktop already provides — end users don't need to install anything.

Tagged releases (`v*`) trigger `.github/workflows/release.yml`, which builds
all three platforms in CI and attaches the zipped artifacts to a draft GitHub
release. See [ROADMAP.md](ROADMAP.md) for the Windows-support feasibility
notes this was based on.

## Project layout

- `xkoranate/` — the application package; module layout mirrors the original
  C++ `src/` tree (paradigms, competitions, xml, eventeditor, signuplisteditor,
  rpeditor, tablegenerator).
- `sports/` — sport definition XML files (copied from the original repo).
- `PORTING.md` — the C++→Python porting conventions used throughout.
- `tests/integration_test.py` — end-to-end boot + scorinate + save/load check.

## Compatibility

- Scorination files (events/RP lists/signups) and table generator files written
  by the original program load unchanged, and files written by this port match
  the original format.
- Settings are stored under the same `thirdgeek.com/xkoranate` identifier, so
  directory preferences from an existing installation carry over.

## License

GNU General Public License v3.0 or later — see [LICENSE](LICENSE). This
project is a derivative of the original xkoranate-CE by Commerce Heights
(ThirdGeek); see [NOTICE.md](NOTICE.md) for full attribution and third-party
components.
