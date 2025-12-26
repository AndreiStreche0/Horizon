import json
import os
from config import DATA_FILE

def load_json():
    # TODO: process the json file if it exists
    if not os.path.exists(DATA_FILE):
        return {"users": {}, "last_user": None}    
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"users": {}, "last_user": None}

def save_json(data):
    # TODO: save data in json file; preferably working with maps
    try:
        os.makedirs("data", exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"The file doesn't exist: {e}")