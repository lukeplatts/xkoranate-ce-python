class XkorSortH2HGoalsAgainstGr:
    def __init__(self, h2hTeams):
        self.l = h2hTeams

    def __call__(self, a, b):
        return a.h2hGoalsAgainst(self.l) < b.h2hGoalsAgainst(self.l)


class XkorSortH2HGoalsAgainstEq:
    def __init__(self, h2hTeams):
        self.l = h2hTeams

    def __call__(self, a, b):
        return a.h2hGoalsAgainst(self.l) == b.h2hGoalsAgainst(self.l)
