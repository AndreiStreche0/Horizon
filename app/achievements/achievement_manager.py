import json
import os
from app.achievements.achievement import Achievement, AchievementTier

class AchievementManager:
    def __init__(self):
        self.achievements = {}
        self.user_achievements = {}  # {username: {achievement_name: tier_name}}
        self.storage_path = "data/achievements_data.json"
        self.init_achievements()
        self._load_store()

    def init_achievements(self):
        achievements_data = [
            ("Barely Alive", "Win the game with less than %d%% health remaining", [15, 10, 5]),
            ("Game Veteran", "Play the game for more than %d minutes", [15, 30, 60]),
            ("Killtacular", "Defeat %d enemies in one single attack", [3, 5, 7]),
            ("Master Of The Game", "Gain a score higher than %d", [2500, 5000, 10000]),
            ("Sniper", "Defeat at least one enemy from a range of %d pixels or further", [60, 70, 80]),
            ("Speedrunner", "Win a game in %d minutes or less", [7, 6, 5]),
            ("The Human Tank", "Take %d points of damage in total", [1000, 1500, 2000]),
            ("The One Monsters Fear", "Defeat at least %d enemies", [250, 500, 1000]),
            ("Traveler", "Travel at least %d pixels", [20000, 50000, 80000]),
            ("Unstoppable", "Win at least %d games in a row", [2, 4, 8]),
            ("Why Do We Fall", "Die at least %d times", [5, 10, 20]),
            ("Flawless Victory", "Finish at least %d waves without taking any damage in a single game", [2, 3, 5]),
        ]
        for name, description, tiers in achievements_data:
            self.achievements[name] = Achievement(name, description, tiers)

    def _load_store(self):
        os.makedirs("data", exist_ok=True)
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    self.user_achievements = data if isinstance(data, dict) else {}
            except Exception as e:
                print(f"Error loading achievements store: {e}")
                self.user_achievements = {}
        else:
            self.user_achievements = {}

    def _save_store(self):
        try:
            os.makedirs("data", exist_ok=True)
            with open(self.storage_path, "w") as f:
                json.dump(self.user_achievements, f, indent=2)
        except Exception as e:
            print(f"Error saving achievements store: {e}")

    def get_all_achievements(self):
        return list(self.achievements.values())

    def get_achievement(self, name):
        return self.achievements.get(name)

    def load_user_achievements(self, username):
        self._load_store()
        if username not in self.user_achievements:
            self.user_achievements[username] = {}

    def save_user_achievements(self, username):
        self.user_achievements.setdefault(username, {})
        self._save_store()

    def unlock_achievement(self, username, achievement_name, tier):
        self.load_user_achievements(username)
        achievement = self.get_achievement(achievement_name)
        if not achievement:
            return False

        current = self.user_achievements[username].get(achievement_name)
        if current is None or tier.value > AchievementTier[current].value:
            self.user_achievements[username][achievement_name] = tier.name
            self._save_store()
            return True
        return False

    def get_user_achievements(self, username):
        self.load_user_achievements(username)
        user_achvs = []
        for achievement in self.get_all_achievements():
            achv_copy = Achievement(achievement.name, achievement.description, achievement.tiers)
            if achievement.name in self.user_achievements[username]:
                tier_name = self.user_achievements[username][achievement.name]
                achv_copy.unlockedTier = AchievementTier[tier_name]
            user_achvs.append(achv_copy)
        return user_achvs

    def get_achievement_tier(self, username, achievement_name):
        self.load_user_achievements(username)
        tier_name = self.user_achievements[username].get(achievement_name)
        return AchievementTier[tier_name] if tier_name else None