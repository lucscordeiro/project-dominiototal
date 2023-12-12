# player.py
class Player:
    def __init__(self, name):
        self.name = name
        self.territories = []

    def add_territory(self, territory):
        self.territories.append(territory)

    def remove_territory(self, territory):
        self.territories.remove(territory)

    def __str__(self):
        return f"{self.name}"