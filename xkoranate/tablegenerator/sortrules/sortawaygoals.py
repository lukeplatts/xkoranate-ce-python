class XkorSortAwayGoalsGr:
    def __call__(self, a, b):
        return a.awayGoals() > b.awayGoals()


class XkorSortAwayGoalsEq:
    def __call__(self, a, b):
        return a.awayGoals() == b.awayGoals()
