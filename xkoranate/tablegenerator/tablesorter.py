import functools

from .sortrules.sortalpha import XkorSortAlphaEq, XkorSortAlphaGr
from .sortrules.sortawaygoals import XkorSortAwayGoalsEq, XkorSortAwayGoalsGr
from .sortrules.sortgoalaverage import (XkorSortGoalAverageEq,
                                        XkorSortGoalAverageGr)
from .sortrules.sortgoaldifference import (XkorSortGoalDiffEq,
                                           XkorSortGoalDiffGr)
from .sortrules.sortgoalsagainst import (XkorSortGoalsAgainstEq,
                                         XkorSortGoalsAgainstGr)
from .sortrules.sortgoalsfor import XkorSortGoalsForEq, XkorSortGoalsForGr
from .sortrules.sorth2hawaygoals import (XkorSortH2HAwayGoalsEq,
                                         XkorSortH2HAwayGoalsGr)
from .sortrules.sorth2hgoaldifference import (XkorSortH2HGoalDiffEq,
                                              XkorSortH2HGoalDiffGr)
from .sortrules.sorth2hgoalsagainst import (XkorSortH2HGoalsAgainstEq,
                                            XkorSortH2HGoalsAgainstGr)
from .sortrules.sorth2hgoalsfor import (XkorSortH2HGoalsForEq,
                                        XkorSortH2HGoalsForGr)
from .sortrules.sorth2hpoints import XkorSortH2HPointsEq, XkorSortH2HPointsGr
from .sortrules.sorth2hwins import XkorSortH2HWinsEq, XkorSortH2HWinsGr
from .sortrules.sortpoints import XkorSortPointsEq, XkorSortPointsGr
from .sortrules.sortwinpercent import (XkorSortWinPercentEq,
                                       XkorSortWinPercentGr)
from .sortrules.sortwinpercentnfl import (XkorSortWinPercentNFLEq,
                                          XkorSortWinPercentNFLGr)
from .sortrules.sortwinpercentpure import (XkorSortWinPercentPureEq,
                                           XkorSortWinPercentPureGr)
from .sortrules.sortwins import XkorSortWinsEq, XkorSortWinsGr


class XkorTableSorter:
    def __init__(self):
        self.pointsForWin = 0.0
        self.pointsForDraw = 0.0
        self.pointsForLoss = 0.0
        self.h2hTeams = []

    def setH2HTeams(self, teams):
        self.h2hTeams = teams

    def setPointsForWin(self, pts):
        self.pointsForWin = pts

    def setPointsForDraw(self, pts):
        self.pointsForDraw = pts

    def setPointsForLoss(self, pts):
        self.pointsForLoss = pts

    def sort(self, rows, sortType):
        # h2h team list
        l = []
        if sortType[:3] == "h2h":
            for i in rows:
                l.append(i.name())

        if sortType == "alphabetical":
            rval = self.privateSort(rows, XkorSortAlphaGr(), XkorSortAlphaEq())
        elif sortType == "awayGoals":
            rval = self.privateSort(rows, XkorSortAwayGoalsGr(), XkorSortAwayGoalsEq())
        elif sortType == "goalAverage":
            rval = self.privateSort(rows, XkorSortGoalAverageGr(), XkorSortGoalAverageEq())
        elif sortType == "goalDifference":
            rval = self.privateSort(rows, XkorSortGoalDiffGr(), XkorSortGoalDiffEq())
        elif sortType == "goalsAgainst":
            rval = self.privateSort(rows, XkorSortGoalsAgainstGr(), XkorSortGoalsAgainstEq())
        elif sortType == "goalsFor":
            rval = self.privateSort(rows, XkorSortGoalsForGr(), XkorSortGoalsForEq())
        elif sortType == "h2hAwayGoals":
            rval = self.privateSort(rows, XkorSortH2HAwayGoalsGr(l), XkorSortH2HAwayGoalsEq(l))
        elif sortType == "h2hGoalDifference":
            rval = self.privateSort(rows, XkorSortH2HGoalDiffGr(l), XkorSortH2HGoalDiffEq(l))
        elif sortType == "h2hGoalsAgainst":
            rval = self.privateSort(rows, XkorSortH2HGoalsAgainstGr(l), XkorSortH2HGoalsAgainstEq(l))
        elif sortType == "h2hGoalsFor":
            rval = self.privateSort(rows, XkorSortH2HGoalsForGr(l), XkorSortH2HGoalsForEq(l))
        elif sortType == "h2hPoints":
            rval = self.privateSort(rows, XkorSortH2HPointsGr(l), XkorSortH2HPointsEq(l))
        elif sortType == "h2hWins":
            rval = self.privateSort(rows, XkorSortH2HWinsGr(l), XkorSortH2HWinsEq(l))
        elif sortType == "points":
            gr = XkorSortPointsGr(self.pointsForWin, self.pointsForDraw, self.pointsForLoss)
            eq = XkorSortPointsEq(self.pointsForWin, self.pointsForDraw, self.pointsForLoss)
            rval = self.privateSort(rows, gr, eq)
        elif sortType == "winPercent":
            rval = self.privateSort(rows, XkorSortWinPercentGr(), XkorSortWinPercentEq())
        elif sortType == "winPercentNFL":
            rval = self.privateSort(rows, XkorSortWinPercentNFLGr(), XkorSortWinPercentNFLEq())
        elif sortType == "winPercentPure":
            rval = self.privateSort(rows, XkorSortWinPercentPureGr(), XkorSortWinPercentPureEq())
        elif sortType == "wins":
            rval = self.privateSort(rows, XkorSortWinsGr(), XkorSortWinsEq())
        else:
            rval = [list(rows)]
        return rval

    def privateSort(self, rows, gr, eq):
        rval = []
        if len(rows) > 1:
            # sort and place into bins
            rows = sorted(rows, key=functools.cmp_to_key(
                lambda a, b: -1 if gr(a, b) else (1 if gr(b, a) else 0)))
            rval.append([rows[0]])
            for i in range(1, len(rows)):
                if eq(rows[i], rows[i - 1]):
                    rval[-1].append(rows[i])
                else:
                    rval.append([rows[i]])
        elif len(rows) == 1:
            rval.append([rows[0]])
        return rval
