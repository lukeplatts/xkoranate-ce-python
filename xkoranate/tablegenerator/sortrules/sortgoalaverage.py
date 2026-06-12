import sys


class XkorSortGoalAverageGr:
    def __call__(self, a, b):
        gaA = (sys.float_info.max if a.goalsAgainst() == 0
               else a.goalsFor() / a.goalsAgainst())
        gaB = (sys.float_info.max if b.goalsAgainst() == 0
               else b.goalsFor() / b.goalsAgainst())
        return gaA > gaB


class XkorSortGoalAverageEq:
    def __call__(self, a, b):
        gaA = (sys.float_info.max if a.goalsAgainst() == 0
               else a.goalsFor() / a.goalsAgainst())
        gaB = (sys.float_info.max if b.goalsAgainst() == 0
               else b.goalsFor() / b.goalsAgainst())
        return gaA == gaB
