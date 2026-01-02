import json
import os
from config import ACHIVEMENTS_FILE

def load_achievements_data():
    if not os.path.exists(ACHIVEMENTS_FILE):
        return {}
    try:
        with open(ACHIVEMENTS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_achievements_data(data):
    try:
        os.makedirs("data", exist_ok=True)
        with open(ACHIVEMENTS_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"The achievements file doesn't exist: {e}")