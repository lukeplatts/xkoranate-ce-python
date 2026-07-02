"""Crash/launch logging.

Recent Linux launch failures (missing shared libraries, a glibc version too
old for the build) were invisible to users double-clicking the app — no
terminal is attached, so the error just vanishes — and took real trial and
error to reproduce and diagnose. This module makes sure any crash after
Python starts is written to a persistent log file and surfaced to the user,
so a bug report can come with an actual error message attached.

setup() must run before importing anything that could itself fail to import
(PySide6, etc.), so import-time crashes are captured too. It works by
installing sys.excepthook, which Python invokes for any exception that
propagates uncaught to the top of the program — including one raised while
importing a later module — not just ones raised inside setup()'s caller.

This can't catch a crash that happens before Python itself starts (e.g. the
frozen executable failing to load libpython because the system's glibc is
too old) — see the launcher wrapper script for that case.
"""

import logging
import os
import platform
import sys
import traceback
from logging.handlers import RotatingFileHandler

_logger = None


def _logDir():
    if sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Logs")
    elif sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
    else:
        base = os.environ.get("XDG_STATE_HOME", os.path.expanduser("~/.local/state"))
    return os.path.join(base, "xkoranate", "logs")


def logFilePath():
    return os.path.join(_logDir(), "app.log")


def setup():
    global _logger
    if _logger is not None:
        return _logger

    try:
        os.makedirs(_logDir(), exist_ok=True)
        handler = RotatingFileHandler(logFilePath(), maxBytes=1_000_000, backupCount=2, encoding="utf-8")
    except OSError:
        handler = logging.StreamHandler(sys.stderr)

    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger = logging.getLogger("xkoranate")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    try:
        from . import __version__
    except Exception:
        __version__ = "unknown"

    logger.info("xkoranate %s starting on %s / Python %s", __version__, platform.platform(), platform.python_version())
    if sys.platform.startswith("linux"):
        try:
            logger.info("glibc %s", os.confstr("CS_GNU_LIBC_VERSION"))
        except (ValueError, OSError, AttributeError):
            pass

    sys.excepthook = _handleException
    _logger = logger
    return logger


def _handleException(excType, excValue, tb):
    message = "".join(traceback.format_exception(excType, excValue, tb))

    if _logger is not None:
        _logger.error("Unhandled exception:\n%s", message)
    else:
        sys.stderr.write(message)

    _showCrashDialog()


def _showCrashDialog():
    # Only meaningful once Qt has actually started — an exception raised
    # while importing PySide6 itself has nothing to show a dialog with.
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
    except Exception:
        return

    app = QApplication.instance()
    if app is None:
        return

    try:
        box = QMessageBox()
        box.setIcon(QMessageBox.Icon.Critical)
        box.setWindowTitle("xkoranate hit a problem")
        box.setText(
            "xkoranate ran into an unexpected error and needs to close.\n\n"
            "A log file with details was saved to:\n%s\n\n"
            "Please attach that file if you report this issue." % logFilePath()
        )
        box.exec()
    except Exception:
        pass
