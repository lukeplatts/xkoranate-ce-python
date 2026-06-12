import sys

from PySide6.QtCore import QFile, QIODevice, QXmlStreamReader

from ..sport import XkorSport
from ..variant import toDouble, toInt


class XkorXmlSportReader(QXmlStreamReader):
    def __init__(self, filename):
        super().__init__()
        self.m_sport = XkorSport()
        self.m_filename = filename

        f = QFile(self.m_filename)
        if not f.exists():
            self.raiseError("File ‘%s’ not found by XkorXmlSportReader::XkorXmlSportReader(QString)" % self.m_filename)
            return
        f.open(QIODevice.ReadOnly)
        self.setDevice(f)

        while not self.atEnd():
            if self.isStartElement():
                if self.name() == "sport" and self.attributes().value("version") == "0.3":
                    self.readFile()
                else:
                    self.raiseError("The file ‘%s’ is not an xkoranate version 0.3 sport." % self.m_filename)
            self.readNext()

        if self.hasError():
            print(self.error(), file=sys.stderr)

        f.close()

    def error(self):
        err = QXmlStreamReader.error(self)
        if err == QXmlStreamReader.Error.NoError:
            return ""  # no error
        elif err == QXmlStreamReader.Error.UnexpectedElementError:
            rval = "An unexpected element was found."
        elif err == QXmlStreamReader.Error.NotWellFormedError:
            rval = "The input file was not well-formed XML."
        elif err == QXmlStreamReader.Error.PrematureEndOfDocumentError:
            rval = "The document ended unexpectedly."
        else:  # CustomError
            rval = self.errorString()
        rval += "\nError occured at line %s, column %s of ‘%s’." % (str(self.lineNumber()), str(self.columnNumber()), self.m_filename)
        return rval

    def readDataPoints(self):
        rval = {}  # QMap<double, double>: iterate sorted(rval.items())

        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == "dataPoint":
                    pos = toDouble(self.attributes().value("pos"))
                    rval[pos] = self.readDouble()
                else:
                    self.readUnknownElement()
        return rval

    def readDouble(self):
        return toDouble(self.readElementText())

    def readFile(self):
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == "name":
                    self.m_sport.setName(self.readString())
                elif self.name() == "alphabetizedName":
                    self.m_sport.setAlphabetizedName(self.readString())
                elif self.name() == "discipline":
                    self.m_sport.setDiscipline(self.readString())
                elif self.name() == "event":
                    self.m_sport.setEvent(self.readString())
                elif self.name() == "scorinator":
                    self.m_sport.setScorinator(self.readString())
                elif self.name() == "paradigm":
                    self.m_sport.setParadigm(self.readString())
                elif self.name() == "paradigmOptions":
                    options = self.readOptions()
                    self.m_sport.setParadigmOptions(options)
                elif self.name() == "dataPoints":
                    name = self.attributes().value("name")
                    dataPoints = self.readDataPoints()
                    self.m_sport.addDataPoints(name, dataPoints)
                else:
                    self.readUnknownElement()

    def readInt(self):
        return toInt(self.readElementText())

    def readList(self):
        rval = []
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == "double":
                    value = self.readDouble()
                    rval.append(value)
                elif self.name() == "int":
                    value = self.readInt()
                    rval.append(value)
                elif self.name() == "list":
                    value = self.readList()
                    rval.append(value)
                elif self.name() == "string":
                    value = self.readString()
                    rval.append(value)
                else:
                    self.readUnknownElement()
        # self.readNext()  # skip end element
        return rval

    def readOptions(self):
        rval = {}
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                type = self.attributes().value("type")
                if self.name() == "double":
                    value = self.readDouble()
                    rval[type] = value
                elif self.name() == "int":
                    value = self.readInt()
                    rval[type] = value
                elif self.name() == "list":
                    value = self.readList()
                    rval[type] = value
                elif self.name() == "string":
                    value = self.readString()
                    rval[type] = value
                else:
                    self.readUnknownElement()
        return rval

    def readString(self):
        return self.readElementText()

    def readUnknownElement(self):
        while not self.atEnd():
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                self.readUnknownElement()

    def sport(self):
        return self.m_sport
