SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Horizon"

#Temporary data, they can change
COLOR_BACKGROUND_MENU = (30, 30, 40) # Dark Blue-ish
COLOR_TEXT = (255, 255, 255)

PLAYABLE_CHARACTERS = {
    "knight": {
        "name": "Knight",
        "description": "Balanced warrior",
        "folder": "knight",
        "hp": 100,
        "speed": 300,
        "damage": 25,
        "animations_frames": {
            "idle": 6,
            "run": 8,
            "attack1": 7,
            "attack2": 10,
            "attack3": 11,
            "hurt": 4,
            "death": 4
        }
    },
    "templar": {
        "name": "Templar",
        "description": "Heavy armored fighter",
        "folder": "templar",
        "hp": 150,
        "speed": 250,
        "damage": 20,
        "animations_frames": {
            "idle": 6,
            "run": 8,
            "attack1": 7,
            "attack2": 8,
            "attack3": 11,
            "hurt": 4,
            "death": 4
        }
    },
    "axeman": {
        "name": "Axeman",
        "description": "High damage dealer",
        "folder": "axeman",
        "hp": 80,
        "speed": 350,
        "damage": 30,
        "animations_frames": {
            "idle": 6,
            "run": 8,
            "attack1": 9,
            "attack2": 9,
            "attack3": 12,
            "hurt": 4,
            "death": 4
        }
    }
}