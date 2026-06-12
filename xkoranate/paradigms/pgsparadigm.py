import sys

from ..result import XkorResult
from ..variant import toDouble, toInt, toList, toString
from .timedparadigm import XkorTimedParadigm


class XkorPGSParadigm(XkorTimedParadigm):
    def __init__(self, sport=None, userOptions=None):
        super().__init__(sport, userOptions)
        self.supportedCompetitions = {}
        self.supportedCompetitions["matches"] = True

    def newOptionsWidget(self, paradigmOptions):
        from .options.pgsparadigmoptions import XkorPGSParadigmOptions
        return XkorPGSParadigmOptions(paradigmOptions)

    def calculateTotal(self, r):
        attempts = toList(r.result.get("attempts"))
        attemptStrings = toList(r.result.get("attemptStrings"))
        r.setScore(toDouble(attempts[len(attempts) - 1]))
        r.setScoreString(toString(attemptStrings[len(attemptStrings) - 1]))

        r.setOutput(self.outputLine(r))

    def formatScore(self, score):
        return "+" + XkorTimedParadigm.formatScore(self, score)

    def outputLine(self, r):
        nameWidth = toInt(self.userOpt.get("nameWidth", 20)) + 2
        resultWidth = toInt(self.opt.get("resultWidth", 5)) + 2

        rval = self.formatName(r.athlete.name, r.athlete.nation).ljust(nameWidth)
        attemptStrings = toList(r.value("attemptStrings"))
        for i in attemptStrings:
            rval += toString(i).rjust(resultWidth)

        return rval

    def scorinate(self, athletes, previousResults=None):
        # initialize results
        self.out = []
        self.res = []

        acc = 0
        for awayIdx in range(len(athletes)):
            if acc & 1:
                away = athletes[awayIdx]
                home = athletes[awayIdx - 1]  # home = away - 1

                homeResult = XkorResult()
                awayResult = XkorResult()
                homeResult.athlete = home.clone()
                awayResult.athlete = away.clone()

                for i in range(toInt(self.opt.get("attempts", 1))):
                    # scorinate the home result
                    result = self.individualResult(home, "score")
                    attempts = toList(homeResult.result.get("attempts"))
                    attemptStrings = toList(homeResult.result.get("attemptStrings"))
                    attempts.append(result.score())
                    attemptStrings.append(result.scoreString())
                    homeResult.result["attempts"] = attempts
                    homeResult.result["attemptStrings"] = attemptStrings

                    # scorinate the away result
                    result = self.individualResult(away, "score")
                    attempts = toList(awayResult.result.get("attempts"))
                    attemptStrings = toList(awayResult.result.get("attemptStrings"))
                    attempts.append(result.score())
                    attemptStrings.append(result.scoreString())
                    awayResult.result["attempts"] = attempts
                    awayResult.result["attemptStrings"] = attemptStrings

                # sort out PGS stuff
                totalHomeScore = 0.0
                totalAwayScore = 0.0
                thisScore = 0.0
                maxScore = toDouble(self.userOpt.get("maxScore", 1.5))
                for i in range(toInt(self.opt.get("attempts", 1))):
                    if toList(homeResult.value("attempts"))[i] == sys.float_info.max:
                        totalHomeScore = maxScore
                        totalAwayScore = 0
                        attempts = toList(awayResult.result.get("attempts"))
                        attemptStrings = toList(awayResult.result.get("attemptStrings"))
                        attempts[i] = 0
                        attemptStrings[i] = ""
                        awayResult.result["attempts"] = attempts
                        awayResult.result["attemptStrings"] = attemptStrings
                    elif toList(awayResult.value("attempts"))[i] == sys.float_info.max:
                        totalAwayScore = maxScore
                        totalHomeScore = 0
                        attempts = toList(homeResult.result.get("attempts"))
                        attemptStrings = toList(homeResult.result.get("attemptStrings"))
                        attempts[i] = 0
                        attemptStrings[i] = ""
                        homeResult.result["attempts"] = attempts
                        homeResult.result["attemptStrings"] = attemptStrings
                    else:
                        totalHomeScore += toDouble(toList(homeResult.value("attempts"))[i])
                        totalAwayScore += toDouble(toList(awayResult.value("attempts"))[i])
                        if totalHomeScore > totalAwayScore:
                            totalHomeScore -= totalAwayScore
                            thisScore = totalHomeScore
                            if totalHomeScore > maxScore:
                                totalHomeScore = maxScore
                            totalAwayScore = 0

                            attempts = toList(homeResult.result.get("attempts"))
                            attemptStrings = toList(homeResult.result.get("attemptStrings"))
                            attempts[i] = thisScore
                            attemptStrings[i] = self.formatScore(thisScore)
                            homeResult.result["attempts"] = attempts
                            homeResult.result["attemptStrings"] = attemptStrings

                            attempts = toList(awayResult.result.get("attempts"))
                            attemptStrings = toList(awayResult.result.get("attemptStrings"))
                            attempts[i] = 0
                            attemptStrings[i] = ""
                            awayResult.result["attempts"] = attempts
                            awayResult.result["attemptStrings"] = attemptStrings
                        else:
                            totalAwayScore -= totalHomeScore
                            thisScore = totalAwayScore
                            if totalAwayScore > maxScore:
                                totalAwayScore = maxScore
                            totalHomeScore = 0

                            attempts = toList(homeResult.result.get("attempts"))
                            attemptStrings = toList(homeResult.result.get("attemptStrings"))
                            attempts[i] = 0
                            attemptStrings[i] = ""
                            homeResult.result["attempts"] = attempts
                            homeResult.result["attemptStrings"] = attemptStrings

                            attempts = toList(awayResult.result.get("attempts"))
                            attemptStrings = toList(awayResult.result.get("attemptStrings"))
                            attempts[i] = thisScore
                            attemptStrings[i] = self.formatScore(thisScore)
                            awayResult.result["attempts"] = attempts
                            awayResult.result["attemptStrings"] = attemptStrings
                    print(totalHomeScore, totalAwayScore, file=sys.stderr)

                homeResult.setOutput(self.outputLine(homeResult))
                awayResult.setOutput(self.outputLine(awayResult) + "\n")

                self.res.append(homeResult)
                self.res.append(awayResult)
            acc += 1

        self.generateOutput()
