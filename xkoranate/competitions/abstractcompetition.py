import math

from xkoranate.athlete import XkorAthlete
from xkoranate.result import XkorResult
from xkoranate.sport import XkorSport
from xkoranate.startlist import XkorStartList, XkorStartListGroup
from xkoranate.variant import toString


class XkorAbstractCompetition:
    def __init__(self, sl=None, s=None, paradigmOptions=None, competitionOptions=None, results=None):
        self.resultsBuf = {}  # QHash<int, QString>
        self.resumeOpt = {}
        self.userOpt = {}
        self.startList = XkorStartList()
        self.sport = XkorSport()
        self.paradigmOpt = {}
        if sl is not None:
            self.init(sl, s, paradigmOptions, competitionOptions, results)

    def hasOptionsWidget(self):
        return False

    def init(self, sl, s, paradigmOptions, competitionOptions, results):
        # C++ copies the start list by value; copy the group structure so that
        # later changes to the caller's start list don't leak into us
        self.startList = XkorStartList()
        self.startList.name = sl.name
        self.startList.groups = [XkorStartListGroup(g.name, list(g.athletes)) for g in sl.groups]
        self.sport = s
        self.paradigmOpt = dict(paradigmOptions)
        self.userOpt = dict(competitionOptions)
        self.resultsBuf = dict(results)

    def matchdays(self):
        raise NotImplementedError  # pure virtual

    def matchdayNames(self):
        raise NotImplementedError  # pure virtual

    def nameWidth(self):
        maximumWidth = 20
        showTeamNames = 1 if toString(self.paradigmOpt.get("showTLAs", "true")) == "true" else 0
        groups = self.startList.groups
        for i in groups:
            for j in i.athletes:
                if len(j.name) + showTeamNames * (3 + len(j.nation)) > maximumWidth:
                    maximumWidth = len(j.name) + showTeamNames * (3 + len(j.nation))
        return maximumWidth

    def newOptionsWidget(self, options):
        return None

    def schedule(self):
        """Full fixture list across every matchday, before any results are
        generated. Returns None for competition types that don't have a
        fixed matchday-vs-matchday schedule (e.g. individually-scored
        events)."""
        return None

    def _formatAthleteName(self, athlete):
        showTLAs = toString(self.paradigmOpt.get("showTLAs", "true")) == "true"
        if showTLAs and athlete.nation:
            return "%s (%s)" % (athlete.name, athlete.nation)
        return athlete.name

    def _formatFixture(self, home, away):
        return "%s v %s" % (self._formatAthleteName(home), self._formatAthleteName(away))

    def rankedListOutput(self, title, results, comparator):
        rankDigits = (int(math.log10(len(results))) + 1) if len(results) > 0 else 1
        rval = " " * (rankDigits + 1) + title + "\n"
        prev = XkorResult()
        for i in range(len(results)):
            # if prev.athlete is set && (prev == results[i] || (!isRankable(prev) && !isRankable(results[i])))
            if (not (prev.athlete == XkorAthlete())) \
                    and ((not comparator(prev, results[i]) and not comparator(results[i], prev))
                         or (not comparator.isRankable(prev) and not comparator.isRankable(results[i]))):
                rval += " " * (rankDigits + 1) + results[i].output() + "\n"
            elif not comparator.isRankable(results[i]) and comparator.isRankable(prev):
                rval += "—".rjust(rankDigits) + " " + results[i].output() + "\n"
            else:
                rval += str(i + 1).rjust(rankDigits) + " " + results[i].output() + "\n"
            prev = results[i]
        rval += "\n"
        return rval

    def results(self, matchday):
        return self.resultsBuf.get(matchday, "")

    def resumeFileOptions(self):
        return dict(self.resumeOpt)

    def revertToMatchday(self, matchday):
        # given matchday is the first that will be erased
        return {}

    def scorinate(self, matchday):
        raise NotImplementedError  # pure virtual
