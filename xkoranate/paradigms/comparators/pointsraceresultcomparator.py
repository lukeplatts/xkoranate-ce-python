from ...variant import toDouble
from .basicresultcomparator import XkorBasicResultComparator


class XkorPointsRaceResultComparator(XkorBasicResultComparator):
    def __init__(self, type, opt):
        super().__init__(type, opt)

    def __call__(self, a, b):
        if a.score() > b.score():
            return True
        elif a.score() == b.score() and toDouble(a.value("laps")) > toDouble(b.value("laps")):
            return True
        elif (a.score() == b.score() and a.value("laps") == b.value("laps")
              and toDouble(a.value("time")) > toDouble(b.value("time"))):
            return True
        else:
            return False

    def sort(self, res):
        res.sort(key=self.sortKey())
