from storage.io import load_json, save_json

class AuthentificationManager:
    def __init__(self):
        #TODO change last_user logic with anonymous logic after adding log in option
        self.user_data = load_json()
        self.current_user = self.user_data.get("last_user", "Player")
        
        if self.current_user not in self.user_data["users"]:
            self.create_user(self.current_user)

    def login(self, username):
        self.current_user = username
        if username not in self.user_data["users"]:
            self.create_user(username)
        
        self.user_data["last_user"] = username
        save_json(self.user_data)

    def create_user(self, username):
        self.user_data["users"][username] = 0
        save_json(self.user_data)

    def get_current_high_score(self):
        return self.user_data["users"].get(self.current_user, 0)

    def save_new_score(self, new_score):
        high_score = self.get_current_high_score()
        
        if new_score > high_score:
            self.user_data["users"][self.current_user] = new_score
            save_json(self.user_data)
            return True
        return False
    
    def get_all_user_scores(self):
        users_dictionary = self.user_data.get("users", {})
        
        return sorted(users_dictionary.items(), key=lambda item: item[1], reverse=True)