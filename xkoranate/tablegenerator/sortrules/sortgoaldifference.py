class XkorSortGoalDiffGr:
    def __call__(self, a, b):
        return a.goalDifference() > b.goalDifference()


class XkorSortGoalDiffEq:
    def __call__(self, a, b):
        return a.goalDifference() == b.goalDifference()
