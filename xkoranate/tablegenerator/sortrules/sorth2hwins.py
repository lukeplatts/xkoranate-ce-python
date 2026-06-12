class XkorSortH2HWinsGr:
    def __init__(self, h2hTeams):
        self.l = h2hTeams

    def __call__(self, a, b):
        return a.h2hWins(self.l) > b.h2hWins(self.l)


class XkorSortH2HWinsEq:
    def __init__(self, h2hTeams):
        self.l = h2hTeams

    def __call__(self, a, b):
        return a.h2hWins(self.l) == b.h2hWins(self.l)
