import sys

from PySide6.QtCore import QDir, QDirIterator

from ..exceptions import XkorFileNotFoundException, XkorSearchFailedException
from .xmlsportreader import XkorXmlSportReader


class XkorXmlIndex:
    def __init__(self):
        self.index = {}  # std::map<QString, QString>: sorted by key

    def insert(self, filename):
        # parse the XML file
        r = XkorXmlSportReader(filename)
        if r.error() != "":
            print(r.error(), file=sys.stderr)
        else:
            # the key controls alphabetization in the sport list
            # I don’t know why the sport list can’t be sorted explicitly
            self.index[r.sport().alphabetizedName()] = filename

    def traverse(self, dir):
        # initialize a QDir to the desired directory
        d = QDir()
        d.setPath(dir)
        if not d.exists():
            err = "Directory ‘"
            err += d.path()
            err += "’ not found by XkorXmlIndex::traverse(QString)"
            raise XkorFileNotFoundException(err, "sport directory", d.path())
        i = QDirIterator(d, QDirIterator.Subdirectories)
        # iterate
        while i.hasNext():
            f = i.next()
            if i.fileInfo().isFile():
                self.insert(f)

    def lookup(self, name):
        if name not in self.index:
            err = "Unknown object ‘"
            err += name
            err += "’ in XkorXmlIndex::lookup(QString)"
            raise XkorSearchFailedException(err)
        return self.index[name]

    def getAllFiles(self):
        # std::map iterates in sorted-key order
        return dict(sorted(self.index.items()))
