# RECOMMENDED SIZES 
#1. Retro: 800 x 600
#2. Small: 1024 x 768
#3. Big: 1280 x 720
#4. Large Monitor: 1600 x 900
#5. Default: 1920 x 1080
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Horizon"

#Temporary data, they can change
COLOR_BACKGROUND_MENU = (30, 30, 40)
COLOR_TEXT = (255, 255, 255)
NUMBER_OF_WAVES = 2
PLAYERS_FILE = "data/player_data.json"
ACHIVEMENTS_FILE = "data/achievements_data.json"
PLAYABLE_CHARACTERS = {
    "knight": {
        "name": "Knight",
        "description": "Balanced warrior",
        "folder": "knight",
        "hp": 100,
        "speed": 10,
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
        "speed": 15,
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
        "speed": 20,
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
ENEMY_SPEED = 0.5

MAP_WIDTH = 2280
MAP_HEIGHT = 1560
