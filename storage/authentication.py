import json
from pathlib import Path
import bcrypt

class AuthenticationManager:
    def __init__(self):
        self.data_file = Path(__file__).resolve().parent.parent / "data" / "player_data.json"
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.players = self.load_players()
    
    def load_players(self):
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_players(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.players, f, indent=4)
    
    def _hash_password(self, password):
        salt = bcrypt.gensalt(rounds=10)
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def player_exists(self, username):
        return username in self.players
    
    def create_player(self, username, password=""):
        if self.player_exists(username):
            return False

        self.players[username] = {
            "password": self._hash_password(password),
            "best_score": 0,
            "games_played": 0,
            "total_time_played": 0,
            "damage_taken": 0,
            "enemies_defeated": 0,
            "distance_traveled": 0,
            "win_streak": 0,
            "best_win_streak": 0,
            "deaths": 0
        }
        self.save_players()
        return True

    def validate_user(self, username, password=""):
        if not self.player_exists(username):
            return False
        hashed = self.players[username].get("password", "")
        return self._verify_password(password, hashed)

    def login_or_create(self, username, password=""):
        if not username:
            return False, None

        if self.player_exists(username):
            if self.validate_user(username, password):
                return True, self.players[username]
            return False, None

        self.create_player(username, password)
        return True, self.players[username]

    def get_or_create_player(self, username):
        if not self.player_exists(username):
            self.create_player(username, "")
        return self.players[username]

    def get_player_best_score(self, username):
        if username in self.players:
            return self.players[username].get("best_score", 0)
        return 0