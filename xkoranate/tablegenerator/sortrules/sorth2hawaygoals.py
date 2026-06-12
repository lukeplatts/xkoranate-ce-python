class XkorSortH2HAwayGoalsGr:
    def __init__(self, h2hTeams):
        self.l = h2hTeams

    def __call__(self, a, b):
        return a.h2hAwayGoals(self.l) > b.h2hAwayGoals(self.l)


class XkorSortH2HAwayGoalsEq:
    def __init__(self, h2hTeams):
        self.l = h2hTeams

    def __call__(self, a, b):
        return a.h2hAwayGoals(self.l) == b.h2hAwayGoals(self.l)
