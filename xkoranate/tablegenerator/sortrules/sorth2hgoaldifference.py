class XkorSortH2HGoalDiffGr:
    def __init__(self, h2hTeams):
        self.l = h2hTeams

    def __call__(self, a, b):
        return a.h2hGoalDifference(self.l) > b.h2hGoalDifference(self.l)


class XkorSortH2HGoalDiffEq:
    def __init__(self, h2hTeams):
        self.l = h2hTeams

    def __call__(self, a, b):
        return a.h2hGoalDifference(self.l) == b.h2hGoalDifference(self.l)
