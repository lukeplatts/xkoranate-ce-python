class XkorSortGoalsAgainstGr:
    def __call__(self, a, b):
        return a.goalsAgainst() < b.goalsAgainst()


class XkorSortGoalsAgainstEq:
    def __call__(self, a, b):
        return a.goalsAgainst() == b.goalsAgainst()
