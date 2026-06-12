from ..abstracttreewidget import XkorAbstractTreeWidget


class XkorAbstractRPBonusWidget(XkorAbstractTreeWidget):
    def bonuses(self):
        raise NotImplementedError  # pure virtual

    def maxBonus(self):
        return 1

    def minBonus(self):
        return 0

    def options(self):
        return {}

    def setBonuses(self, bonuses):
        raise NotImplementedError  # pure virtual

    def setMaxBonus(self, newMax):
        pass

    def setMinBonus(self, newMin):
        pass

    def setOptions(self, options):
        pass

    def setUseParticipantBonus(self, use=True):
        raise NotImplementedError  # pure virtual

    def setUseTeamBonus(self, use=True):
        raise NotImplementedError  # pure virtual
