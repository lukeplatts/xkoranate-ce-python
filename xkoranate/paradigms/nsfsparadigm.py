import math

from ..variant import toDouble, toInt, toString
from .abstracth2hparadigm import XkorAbstractH2HParadigm


class XkorNSFSParadigm(XkorAbstractH2HParadigm):
    def __init__(self, sport=None, userOptions=None):
        super().__init__(sport, userOptions)

    def hasOptionsWidget(self):
        return True

    def newOptionsWidget(self, paradigmOptions):
        from .options.nsfsparadigmoptions import XkorNSFSParadigmOptions
        return XkorNSFSParadigmOptions(paradigmOptions, self._defaultHomeAdvantageMagnitude())

    def _defaultHomeAdvantageMagnitude(self):
        return toDouble(self.opt.get("homeAdvantage", 4.0 / 3.0))

    def homeAdvantageMagnitude(self):
        # the sport file provides a default magnitude; the options widget
        # lets the user override it per-event
        return toDouble(self.userOpt.get("homeAdvantageMagnitude", self._defaultHomeAdvantageMagnitude()))

    # protected:

    def generateScore(self, skill, oppSkill, style, oppStyle,
                      homeAdvantage=False, attackMultiplier=1):
        # load constants
        baseAttackCoeff = toDouble(self.opt.get("baseAttackCoeff"))
        rankDiffModifier = toDouble(self.opt.get("rankDiffModifier"))
        rankCoeff = toDouble(self.opt.get("rankCoeff"))
        rankScalar = toDouble(self.opt.get("rankScalar"))
        bast = toDouble(self.opt.get("baseAttackSuccessThreshold"))
        baseAttacksSuperior = toInt(self.opt.get("baseAttacksSuperior"))
        baseAttacksInferior = toInt(self.opt.get("baseAttacksInferior"))
        attackCoeffSuperior = toDouble(self.opt.get("attackCoeffSuperior"))
        attackCoeffInferior = toDouble(self.opt.get("attackCoeffInferior"))
        homeAdvValue = (self.homeAdvantageMagnitude() if homeAdvantage else 1)

        if skill > oppSkill:
            attacks = int((baseAttacksSuperior + ((skill - oppSkill) * attackCoeffSuperior))
                          * attackMultiplier)
        else:
            attacks = int((baseAttacksInferior + ((skill - oppSkill) * attackCoeffInferior))
                          * attackMultiplier)

        # calculate P(goal) on any given attack
        pGoal = 1 - ((bast + rankDiffModifier
                      * (math.pow(oppSkill * rankCoeff, rankScalar)
                         - math.pow(skill * rankCoeff, rankScalar)))
                     / (baseAttackCoeff * homeAdvValue))

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

    def generateStyleModification(self, homeScore, awayScore, homeStyle, awayStyle):
        if toString(self.userOpt.get("NSFSStyleMods", "true")) == "true":
            styleCoeffA = toDouble(self.opt.get("NSFSStyleCoeffA", 2.0991677816057))
            styleCoeffB = toDouble(self.opt.get("NSFSStyleCoeffB", 1.2442581729602))
            styleExponent = toDouble(self.opt.get("NSFSStyleExponent", -0.42705203296846))
            styleOffset = toDouble(self.opt.get("NSFSStyleOffset", 0.072435335725325))

            styleModifier = (homeStyle + awayStyle) / 2.0 + self.s.randGaussian()
            result = homeScore - awayScore

            styleMultiplier = (styleCoeffA
                               / (1 + styleCoeffB * math.pow(math.e, styleExponent * styleModifier))
                               + styleOffset)

            homeScore = int(homeScore * styleMultiplier)
            awayScore = int(awayScore * styleMultiplier)

            # if a negative style modifier changed the result to a draw, fix it
            if homeScore == awayScore and result > 0:
                homeScore += 1
            elif homeScore == awayScore and result < 0:
                awayScore += 1

            return (homeScore, awayScore)
        else:
            styleEffect = 0
            # what’s the maximum change we can make that will preserve W/D/L?
            maxStyleEffect = ((0 if homeScore == awayScore else abs(homeScore - awayScore) - 1)
                              + min(homeScore, awayScore))
            styleEffect = int(self.s.individualScore("style", (homeStyle + awayStyle) / 20 + 0.5))
            if styleEffect < -maxStyleEffect:
                styleEffect = -maxStyleEffect
            homeScore += max(-homeScore, styleEffect)  # don’t drop the score below 0
            awayScore += max(-awayScore, styleEffect)  # don’t drop the score below 0
            return (homeScore, awayScore)
