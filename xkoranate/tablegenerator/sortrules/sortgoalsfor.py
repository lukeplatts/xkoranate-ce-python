class XkorSortGoalsForGr:
    def __call__(self, a, b):
        return a.goalsFor() > b.goalsFor()


class XkorSortGoalsForEq:
    def __call__(self, a, b):
        return a.goalsFor() == b.goalsFor()
