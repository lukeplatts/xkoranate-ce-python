class XkorSortWinPercentNFLGr:
    def __call__(self, a, b):
        wpA = 0 if a.played() == 0 else a.wins() / (a.wins() + a.losses())
        wpB = 0 if b.played() == 0 else b.wins() / (b.wins() + b.losses())
        return wpA > wpB


class XkorSortWinPercentNFLEq:
    def __call__(self, a, b):
        wpA = 0 if a.played() == 0 else a.wins() / (a.wins() + a.losses())
        wpB = 0 if b.played() == 0 else b.wins() / (b.wins() + b.losses())
        return wpA == wpB
