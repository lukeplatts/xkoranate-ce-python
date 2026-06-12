import copy

from .athlete import XkorAthlete
from .variant import qNumber, toDouble, toString


class XkorResult:
    def __init__(self, score=None, scoreString=None, ath=None):
        self.athlete = ath if ath is not None else XkorAthlete()
        self.result = {}
        if score is not None:
            self.setScore(score)
        if scoreString is not None:
            self.setScoreString(scoreString)

    def clone(self):
        r = XkorResult()
        r.athlete = self.athlete.clone()
        r.result = copy.copy(self.result)
        return r

    def contains(self, key):
        return key in self.result

    def output(self):
        return toString(self.result.get("output", ""))

    def score(self):
        return toDouble(self.result.get("score"))

    def scoreString(self):
        if "scoreString" in self.result:
            return toString(self.result["scoreString"])
        else:
            return qNumber(self.score())

    def setOutput(self, s):
        self.result["output"] = s

    def setScore(self, s):
        self.result["score"] = s

    def setScoreString(self, s):
        self.result["scoreString"] = s

    def value(self, key):
        return self.result.get(key)

    def __eq__(self, b):
        return isinstance(b, XkorResult) and self.athlete.id == b.athlete.id
