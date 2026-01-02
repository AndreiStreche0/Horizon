from storage.achievements_io import load_achievements_data, save_achievements_data
from app.achievements.achievement import Achievement, ACHIEVEMENT_LIST

class AchievementManager:
    def __init__(self, brain):
        self.brain = brain
        self.achievement_data = load_achievements_data()

    #for UI
    def _get_user_data(self):
        user = self.brain.username
        if user not in self.achievement_data:
            self.achievement_data[user] = {}
        return self.achievement_data[user]
    def achievement_progress(self, name):
        user_data = self._get_user_data()
        val = user_data.get(name, 0)
        #for unitialized reverse values
        if (name == "Speed Runner" or name == "Barely Alive") and val == 0:
            val = 9999999
        return val
    def get_achievement(self, name):
        for a in ACHIEVEMENT_LIST:
            if a.name == name:
                return a
        return None
                
    def update(self, name, value):
        current = self.achievement_progress(name)

        new_val = current

        achievement = self.get_achievement(name)
        if achievement.type == "total":
            new_val = current + value
        elif achievement.type == "max":
            if achievement.reverse:
                if value < current:
                    new_val = value
            else:
                if value > current:
                    new_val = value

        if new_val != current:
            self.achievement_data[self.brain.username][name] = new_val
            save_achievements_data(self.achievement_data)

    #returns color and next goal
    def get_medal_info(self, name):
        val = self.achievement_progress(name)
        achievement = self.get_achievement(name)
        
        bronze, silver, gold = achievement.tiers
        
        if achievement.reverse:
            if val <= gold: return ("GOLD", "Completed")
            if val <= silver: return ("SILVER", f"Goal : < {gold}")
            if val <= bronze: return ("BRONZE", f"Goal : < {silver}")
            return ("NONE", f"Goal : < {bronze}")
        else:
            if val >= gold: return ("GOLD", "Completed")
            if val >= silver: return ("SILVER", f"Goal : {gold}")
            if val >= bronze: return ("BRONZE", f"Goal : {silver}")
            return ("NONE", f"Goal : {bronze}")