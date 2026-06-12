class XkorFileNotFoundException(Exception):
    def __init__(self, errorText, fileType, fileName):
        super().__init__(errorText)
        self._type = fileType
        self._name = fileName

    def fileType(self):
        return self._type

    def fileName(self):
        return self._name


class XkorSearchFailedException(Exception):
    pass
