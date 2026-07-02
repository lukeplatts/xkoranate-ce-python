import math

from ..variant import toDouble
from .abstracth2hparadigm import XkorAbstractH2HParadigm


class XkorSQISParadigm(XkorAbstractH2HParadigm):
    def __init__(self, sport=None, userOptions=None):
        super().__init__(sport, userOptions)

    def hasOptionsWidget(self):
        return True

    def newOptionsWidget(self, paradigmOptions):
        from .options.sqisparadigmoptions import XkorSQISParadigmOptions
        return XkorSQISParadigmOptions(paradigmOptions)

    def homeAdvantageMagnitude(self):
        # the sport file provides a default magnitude; the options widget
        # lets the user override it per-event
        default = toDouble(self.opt.get("homeAdvantage", 4.0 / 3.0))
        return toDouble(self.userOpt.get("homeAdvantageMagnitude", default))

    # protected:

    def generateScore(self, skill, oppSkill, style, oppStyle,
                      homeAdvantage=False, attackMultiplier=1):
        # add 0.5 so that values can be rounded up
        attacks = int(toDouble(self.opt.get("attacks")) * attackMultiplier + 0.5)

        a = toDouble(self.opt.get("constantA"))
        b = toDouble(self.opt.get("constantB"))
        homeAdvValue = (self.homeAdvantageMagnitude() if homeAdvantage else 1)

        # calculate P(goal) on any given attack
        pGoal = (a + (b - (1 if skill == oppSkill else min(skill, oppSkill) / max(skill, oppSkill)) * b)
                 * (1 if skill > oppSkill else -1)) * homeAdvValue

        # score
        rand = self.s.randUniform()
        acc = 0.0
        pIGoals = math.pow(1 - pGoal, attacks)  # probability of 0 goals
        for i in range(attacks + 1):
            acc += pIGoals
            if rand < acc:
                return i
            # calculate probability of i + 1 goals
            pIGoals *= (attacks - i) * pGoal / ((i + 1) * (1 - pGoal))
        return -1
