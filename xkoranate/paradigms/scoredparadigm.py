from ..variant import toInt
from .timedparadigm import XkorTimedParadigm


class XkorScoredParadigm(XkorTimedParadigm):
    def __init__(self, sport=None, userOptions=None):
        super().__init__(sport, userOptions)

    # private:

    def formatScore(self, score):
        return f"{score:.{toInt(self.opt.get('displayDigits'))}f}"
