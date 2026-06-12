"""Locate bundled resources (sports definitions, icons) in dev and frozen runs."""

import os
import sys


def resourceRoot():
    if getattr(sys, "frozen", False):
        # PyInstaller .app: Contents/MacOS/<exe>; resources in Contents/Resources
        bundleDir = os.path.dirname(sys.executable)
        resources = os.path.normpath(os.path.join(bundleDir, "..", "Resources"))
        if os.path.isdir(os.path.join(resources, "sports")):
            return resources
        return getattr(sys, "_MEIPASS", bundleDir)
    # development: repository root (parent of this package)
    return os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


def sportsDir():
    return os.path.join(resourceRoot(), "sports")


def iconsDir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
