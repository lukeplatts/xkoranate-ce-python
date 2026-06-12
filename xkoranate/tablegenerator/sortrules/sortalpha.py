import locale


class XkorSortAlphaGr:
    def __call__(self, a, b):
        # QString::localeAwareCompare(a.name(), b.name()) < 0
        return locale.strcoll(a.name(), b.name()) < 0


class XkorSortAlphaEq:
    def __call__(self, a, b):
        return True  # if we're sorting on alphabetical order, the teams are tied!
