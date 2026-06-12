class XkorGroup:
    def __init__(self, name="", athletes=None):
        self.name = name
        self.athletes = athletes if athletes is not None else []  # list of uuid.UUID

    def clone(self):
        return XkorGroup(self.name, list(self.athletes))
