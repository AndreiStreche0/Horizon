class Achievement:
    def __init__(self, name, description, tiers, type="max", reverse=False):
        self.name = name
        self.description = description
        self.tiers = tiers
        self.type = type    # "total" (over all games) or "max" (single game best)
        self.reverse = reverse #true if lowest value is best
        

ACHIEVEMENT_LIST = [
    Achievement("Game Master", "high score", tiers = [2000, 2500, 3000], type="max"),
    Achievement("Total Killer", "total kills", tiers = [100, 250, 750], type="total"),
    Achievement("Super Tank", "total damage taken", tiers = [5000, 10000, 30000], type="total"),
    Achievement("Game Veteran", "number of hours played", tiers = [5, 10, 25], type="total"),
    Achievement("Total Winner", "number of total wins", tiers = [15, 30, 75], type="total"),
    Achievement("Speed Runner", "fastest win", tiers = [70, 50, 40], type="max", reverse=True),
    Achievement("Distance Traveled", "highest distance",tiers = [5000, 7500, 12000], type="max"),
    Achievement("Barely Alive", "win with HP lower than", tiers = [20, 10, 3], type="max", reverse=True),
    Achievement("Multi Kill", "kills in one attack", tiers = [2, 3, 4], type="max"),
    Achievement("Sniper", "biggest kill range", tiers = [450, 475, 490], type="max"),
]