from ...variant import toString
from .abstractresultcomparator import XkorAbstractResultComparator


class XkorBasicResultComparator(XkorAbstractResultComparator):
    def __init__(self, type, opt):
        super().__init__(type, opt)
        if toString(opt.get("sortOrder", "ascending")) == "ascending":
            self.isAscending = True
        else:
            self.isAscending = False

    def __call__(self, a, b):
        if self.isAscending:
            return a.score() < b.score()
        else:
            return b.score() < a.score()

    def sort(self, res):
        res.sort(key=self.sortKey())
