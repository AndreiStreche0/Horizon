import json
import os
from config import PLAYERS_FILE

def load_json():
    if not os.path.exists(PLAYERS_FILE):
        return {"users": {}, "last_user": None}    
    try:
        with open(PLAYERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"users": {}, "last_user": None}

def save_json(data):
    try:
        os.makedirs("data", exist_ok=True)
        with open(PLAYERS_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"The user data file doesn't exist: {e}")