from xkoranate.competitions.abstractcompetition import XkorAbstractCompetition
from xkoranate.variant import toString


class XkorMassStartCompetition(XkorAbstractCompetition):
    def hasOptionsWidget(self):
        return True

    def matchdays(self):
        return 1

    def matchdayNames(self):
        return ["Mass start"]

    def newOptionsWidget(self, competitionOptions):
        from xkoranate.competitions.options.massstartcompetitionoptions import XkorMassStartCompetitionOptions

        return XkorMassStartCompetitionOptions(competitionOptions)

    def scorinate(self, matchday):
        from xkoranate.paradigms.paradigmfactory import XkorParadigmFactory

        localParadigmOptions = dict(self.paradigmOpt)
        localParadigmOptions["nameWidth"] = self.nameWidth()

        p = XkorParadigmFactory.newParadigmForSport(self.sport, localParadigmOptions)

        allResults = []
        self.resultsBuf[matchday] = ""
        for i in range(len(self.startList.groups)):
            p.scorinate(list(self.startList.groups[i].athletes))
            # C++ copies the results vector before mutating it
            groupResults = [r.clone() for r in p.results()]
            for j in groupResults:
                j.result["heat"] = i  # set the heat number so that the sorting works out correctly
            if toString(self.userOpt.get("sortResults", "true")) == "true":
                p.comparisonFunction().sort(groupResults)
                self.resultsBuf[matchday] += self.rankedListOutput(self.startList.groups[i].name, groupResults, p.comparisonFunction())
            else:
                self.resultsBuf[matchday] += self.startList.groups[i].name + "\n"
                self.resultsBuf[matchday] += p.output() + "\n\n"
            allResults.extend(groupResults)

        # do the complete ranking
        if toString(self.userOpt.get("sortResults", "true")) == "true" and toString(self.userOpt.get("overallRanking", "false")) == "true":
            p.comparisonFunction().sort(allResults)
            self.resultsBuf[matchday] += self.rankedListOutput("Overall ranking", allResults, p.comparisonFunction())
