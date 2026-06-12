import math
import sys

from ..result import XkorResult
from ..variant import qNumber, toDouble, toInt, toString
from .abstractparadigm import XkorAbstractParadigm
from .comparators.pointsraceresultcomparator import XkorPointsRaceResultComparator


class XkorPointsRaceParadigm(XkorAbstractParadigm):
    def __init__(self, sport=None, userOptions=None):
        super().__init__(sport, userOptions)
        self.supportedCompetitions["standard"] = True

    def breakTie(self, athletes, type=""):
        print("unexpected tie break request in points race paradigm", file=sys.stderr)

    def comparisonFunction(self, type=""):
        return XkorPointsRaceResultComparator(type, self.opt)

    def hasOptionsWidget(self):
        return True

    def newOptionsWidget(self, paradigmOptions):
        from .options.timedparadigmoptions import XkorTimedParadigmOptions
        return XkorTimedParadigmOptions(paradigmOptions)

    def scorinate(self, athletes, previousResults=None):
        for i in self.requiredValues:
            if not self.s.hasValue(i):
                print("missing parameter", i,
                      "in XkorPointsRaceParadigm::output(XkorResults *)",
                      file=sys.stderr)
                self.out.append(("", "Sport does not support this paradigm"))
                return

        # initialize results
        self.out = []
        self.res = []

        maxPoints = toInt(self.opt.get("maxPoints"))
        usePoints = (toString(self.opt.get("usePoints", "true")) == "true")

        for i in athletes:
            r = XkorResult()
            r.athlete = i.clone()
            if usePoints:
                r.result["points"] = self.s.individualScore("points", i.rpSkill)
            r.result["laps"] = self.s.individualScore("laps", i.rpSkill)
            r.result["time"] = self.s.randWeighted(i.rpSkill)
            self.res.append(r)

        sum_ = 0.0
        if usePoints:
            for i in self.res:
                sum_ += toDouble(i.value("points"))

        nameWidth = toInt(self.userOpt.get("nameWidth", 20)) + 2
        resultWidth = toInt(self.opt.get("resultWidth", 3)) + 2

        for i in self.res:
            curPoints = 0.0
            if usePoints:
                curPoints = max(0.0, math.floor(toDouble(i.value("points"))
                                                + (maxPoints - sum_) / len(self.res)))
            curLaps = math.floor(toDouble(i.value("laps")) + 0.5)

            status = self.generateStatus()
            if status != "":
                i.setScore(-sys.float_info.max)
                i.setScoreString(status.rjust(resultWidth))
            elif usePoints:
                i.setScore(curPoints + curLaps * 20)
                i.setScoreString(qNumber(curPoints).rjust(resultWidth)
                                 + qNumber(curLaps).rjust(resultWidth))
            else:
                i.setScore(curLaps)
                i.setScoreString(qNumber(curLaps).rjust(resultWidth))

        for i in self.res:
            output = self.formatName(i.athlete.name, i.athlete.nation).ljust(nameWidth)
            output += i.scoreString()
            i.setOutput(output)
            self.out.append((i.athlete.name, output))

    # protected:

    def generateStatus(self):
        statuses = self.readOptionList("statuses")
        statusProbs = self.readOptionList("statusProbs")

        rand = self.s.randUniform()

        acc = 0.0
        for i in range(len(statuses)):
            acc += toDouble(statusProbs[i])
            if rand < acc:
                return toString(statuses[i])
        return ""
