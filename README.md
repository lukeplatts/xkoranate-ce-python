# xkoranate-CE (Python port)

A faithful Python/PySide6 port of [xkoranate-CE](https://github.com/NS-Sports/Xkoranate-CE)
(xkoranate **C**ommunity **E**dition), the sports "scorinator" used by NS Sports,
the sports roleplay forum for NationStates. Originally written in Qt4/C++ by
Commerce Heights/ThirdGeek; this port preserves the original program's behavior —
scorination math, competition formats, file formats and UI — while running on
current macOS via Python and Qt 6.

It simulates results for one hundred–plus disciplines across sixty-plus sports:
mass starts, head-to-head matches, round robins, multi-run events, shooting and
archery formats, and includes the league table generator.

The interface has a modern, light Material-style theme (via `qt-material`) with
Material Design Icons (`qtawesome`); the underlying behaviour is unchanged.

## Running from source

```sh
python3 -m venv .venv
.venv/bin/pip install PySide6 qt-material qtawesome
.venv/bin/python -m xkoranate
```

## Building the macOS app

```sh
.venv/bin/pip install pyinstaller
./build_app.sh          # produces dist/xkoranate.app
```

The app bundles the `sports/` definitions directory into
`xkoranate.app/Contents/Resources/sports/`, same as the original Mac build.
Sport parameter files are plain XML and remain user-editable there. The
PyInstaller spec also bundles the `qt-material` and `qtawesome` data files so
the theme and icons work in the frozen app.

See [ROADMAP.md](ROADMAP.md) for a prioritized list of upstream issues and a
Windows-support feasibility plan.

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

Same terms as the original project (see `GPL`/`LGPL`/`LICENSE` in the upstream
repository).
