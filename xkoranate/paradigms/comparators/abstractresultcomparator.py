import functools
import sys


class XkorAbstractResultComparator:
    def __init__(self, type, opt):
        pass

    def __call__(self, a, b):  # C++ operator()(XkorResult a, XkorResult b)
        raise NotImplementedError

    def isRankable(self, r):
        if r.score() == sys.float_info.max or r.score() == -sys.float_info.max:
            return False
        else:
            return True

    def readOptionList(self, opt, name):
        val = opt.get(name)
        if isinstance(val, list):
            return list(val)
        else:
            return [val]  # create a single-item list

    def sort(self, res):
        raise NotImplementedError

    # port helper: key function for list.sort() emulating qSort/std::sort with
    # this comparator (Python's sort is stable; C++ std::sort was not, which is
    # an acceptable difference)
    def sortKey(self):
        return functools.cmp_to_key(
            lambda a, b: -1 if self(a, b) else (1 if self(b, a) else 0))
