class XkorStartListGroup:
    def __init__(self, name="", athletes=None):
        self.name = name
        self.athletes = athletes if athletes is not None else []  # list of XkorAthlete


class XkorStartList:
    def __init__(self):
        self.name = ""
        self.groups = []  # list of XkorStartListGroup
