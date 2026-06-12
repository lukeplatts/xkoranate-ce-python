class XkorSortWinPercentGr:
    def __call__(self, a, b):
        wpA = 0 if a.played() == 0 else (a.wins() + a.draws() / 2) / a.played()
        wpB = 0 if b.played() == 0 else (b.wins() + b.draws() / 2) / b.played()
        return wpA > wpB


class XkorSortWinPercentEq:
    def __call__(self, a, b):
        wpA = 0 if a.played() == 0 else (a.wins() + a.draws() / 2) / a.played()
        wpB = 0 if b.played() == 0 else (b.wins() + b.draws() / 2) / b.played()
        return wpA == wpB
