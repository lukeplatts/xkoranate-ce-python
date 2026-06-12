import sys

from xkoranate.application import XkorApplication


def main():
    app = XkorApplication(sys.argv)
    app.loadSports()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
