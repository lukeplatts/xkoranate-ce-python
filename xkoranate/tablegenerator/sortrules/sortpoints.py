class XkorSortPointsGr:
    def __init__(self, w, d, l):
        self.pointsForWin = w
        self.pointsForDraw = d
        self.pointsForLoss = l

    def __call__(self, a, b):
        return (a.wins() * self.pointsForWin + a.draws() * self.pointsForDraw
                + a.losses() * self.pointsForLoss
                > b.wins() * self.pointsForWin + b.draws() * self.pointsForDraw
                + b.losses() * self.pointsForLoss)


class XkorSortPointsEq:
    def __init__(self, w, d, l):
        self.pointsForWin = w
        self.pointsForDraw = d
        self.pointsForLoss = l

    def __call__(self, a, b):
        return (a.wins() * self.pointsForWin + a.draws() * self.pointsForDraw
                + a.losses() * self.pointsForLoss
                == b.wins() * self.pointsForWin + b.draws() * self.pointsForDraw
                + b.losses() * self.pointsForLoss)
