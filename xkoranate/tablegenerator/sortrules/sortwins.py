class XkorSortWinsGr:
    def __call__(self, a, b):
        return a.wins() > b.wins()


class XkorSortWinsEq:
    def __call__(self, a, b):
        return a.wins() == b.wins()
