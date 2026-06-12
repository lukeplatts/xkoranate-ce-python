from .timedparadigm import XkorTimedParadigm


class XkorShortTrackParadigm(XkorTimedParadigm):
    def __init__(self, sport=None, userOptions=None):
        super().__init__(sport, userOptions)
        self.supportedCompetitions = {}
        self.supportedCompetitions["standard"] = True

    def newOptionsWidget(self, paradigmOptions):
        from .options.shorttrackparadigmoptions import XkorShortTrackParadigmOptions
        return XkorShortTrackParadigmOptions(paradigmOptions)
