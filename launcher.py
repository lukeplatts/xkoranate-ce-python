"""PyInstaller entry point."""

# Must run before any other xkoranate/PySide6 import — sys.excepthook, once
# installed, still catches an exception raised by the imports below.
from xkoranate import crashlog
crashlog.setup()

from xkoranate.main import main

main()
