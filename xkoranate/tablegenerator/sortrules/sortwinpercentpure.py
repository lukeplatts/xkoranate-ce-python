class XkorSortWinPercentPureGr:
    def __call__(self, a, b):
        wpA = 0 if a.played() == 0 else a.wins() / a.played()
        wpB = 0 if b.played() == 0 else b.wins() / b.played()
        return wpA > wpB


class XkorSortWinPercentPureEq:
    def __call__(self, a, b):
        wpA = 0 if a.played() == 0 else a.wins() / a.played()
        wpB = 0 if b.played() == 0 else b.wins() / b.played()
        return wpA == wpB
