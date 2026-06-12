class XkorSortH2HGoalsForGr:
    def __init__(self, h2hTeams):
        self.l = h2hTeams

    def __call__(self, a, b):
        return a.h2hGoalsFor(self.l) > b.h2hGoalsFor(self.l)


class XkorSortH2HGoalsForEq:
    def __init__(self, h2hTeams):
        self.l = h2hTeams

    def __call__(self, a, b):
        return a.h2hGoalsFor(self.l) == b.h2hGoalsFor(self.l)
