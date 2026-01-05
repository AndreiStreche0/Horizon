import json
from pathlib import Path

class LeaderboardManager:
    def __init__(self):
        self.data_file = Path(__file__).resolve().parent.parent / "data" / "player_data.json"
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.players = self.load_players()

    def load_players(self):
        if self.data_file.exists():
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    for user, pdata in data.items():
                        pdata.setdefault("best_score", 0)
                        pdata.setdefault("games_played", 0)
                        pdata.setdefault("total_time_played", 0)
                        pdata.setdefault("damage_taken", 0)
                        pdata.setdefault("enemies_defeated", 0)
                        pdata.setdefault("total_distance_traveled", 0)
                        pdata.setdefault("win_streak", 0)
                        pdata.setdefault("best_win_streak", 0)
                        pdata.setdefault("deaths", 0)
                    return data
            except Exception:
                return {}
        return {}
    
    def save_players(self):
        with open(self.data_file, "w") as f:
            json.dump(self.players, f, indent=4)

    def add_score(self, username, score, session_time=0, session_damage=0, session_enemies=0, session_distance=0, is_dead=False):
        score = int(score)
        session_time = float(session_time or 0)
        session_damage = int(session_damage or 0)
        session_enemies = int(session_enemies or 0)
        session_distance = float(session_distance or 0)

        if username not in self.players:
            self.players[username] = {
                "best_score": score,
                "games_played": 1,
                "total_time_played": session_time,
                "damage_taken": session_damage,
                "enemies_defeated": session_enemies,
                "total_distance_traveled": session_distance,
                "deaths": 1 if is_dead else 0,
            }
            self.save_players()
            return True

        player = self.players[username]
        player["games_played"] = player.get("games_played", 0) + 1
        player["total_time_played"] = player.get("total_time_played", 0) + session_time
        player["damage_taken"] = player.get("damage_taken", 0) + session_damage
        player["enemies_defeated"] = player.get("enemies_defeated", 0) + session_enemies
        player["total_distance_traveled"] = player.get("total_distance_traveled", 0) + session_distance
        if is_dead:
            player["deaths"] = player.get("deaths", 0) + 1

        is_new_high_score = score > player.get("best_score", 0)
        if is_new_high_score:
            player["best_score"] = score

        self.save_players()
        return is_new_high_score

    def get_total_time_played(self, username):
        if username in self.players:
            return int(self.players[username].get("total_time_played", 0))
        return 0

    def get_total_damage_taken(self, username):
        if username in self.players:
            return int(self.players[username].get("damage_taken", 0))
        return 0

    def get_top_scores(self, limit=10):
        sorted_players = sorted(
            self.players.items(),
            key=lambda x: x[1].get("best_score", 0),
            reverse=True,
        )
        return [
            (username, int(data.get("best_score", 0)))
            for username, data in sorted_players[:limit]
        ]

    def get_user_score(self, username):
        if username in self.players:
            return int(self.players[username].get("best_score", 0))
        return 0

    def get_user_rank(self, username):
        sorted_players = sorted(
            self.players.items(),
            key=lambda x: x[1].get("best_score", 0),
            reverse=True,
        )
        for rank, (user, _) in enumerate(sorted_players, 1):
            if user == username:
                return rank
        return None

    def get_user_data(self, username):
        return self.players.get(username, None)

    def get_total_damage_taken(self, username):
        if username in self.players:
            return int(self.players[username].get("damage_taken", 0))
        return 0

    def get_total_enemies_defeated(self, username):
        if username in self.players:
            return int(self.players[username].get("enemies_defeated", 0))
        return 0
    
    def get_total_distance_traveled(self, username):
        if username in self.players:
            return float(self.players[username].get("total_distance_traveled", 0))
        return 0.0

    def update_win_streak(self, username, is_win):
        if username not in self.players:
            return 0
        
        player = self.players[username]
        
        if is_win:
            player["win_streak"] = player.get("win_streak", 0) + 1
        else:
            player["win_streak"] = 0
        
        # Update best_win_streak if current is higher
        if player["win_streak"] > player.get("best_win_streak", 0):
            player["best_win_streak"] = player["win_streak"]
        
        self.save_players()
        return player["best_win_streak"]

    def get_best_win_streak(self, username):
        if username in self.players:
            return int(self.players[username].get("best_win_streak", 0))
        return 0

    def get_current_win_streak(self, username):
        if username in self.players:
            return int(self.players[username].get("win_streak", 0))
        return 0

    def get_total_deaths(self, username):
        if username in self.players:
            return int(self.players[username].get("deaths", 0))
        return 0

    def player_exists(self, username):
        return username in self.players