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
        "speed": 8,
        "damage": 25,
        "animations_frames": {
            "idle": 6,
            "run": 8,
            "attack1": 7,
            "attack2": 10,
            "attack3": 11,
            "hurt": 4,
            "death": 4
        },
        "attacks": {
            "attack1": {
                "frames": [3, 4],
                "hitbox": {
                    "width": 60,
                    "height": 100,
                    "offset_x": 60,
                    "offset_y": -20
                }
            },
            "attack2": {
                "frames": [3, 7],
                "hitbox": {
                    "width": 60,
                    "height": 110,
                    "offset_x": 50,
                    "offset_y": -25
                }
            },
            "attack3": {
                "frames": [7, 8, 9],
                "hitbox": {
                    "width": 120,
                    "height": 120,
                    "offset_x": 85,
                    "offset_y": -30
                }
            }
        },
    },
    "templar": {
        "name": "Templar",
        "description": "Heavy armored fighter",
        "folder": "templar",
        "hp": 150,
        "speed": 10,
        "damage": 20,
        "animations_frames": {
            "idle": 6,
            "run": 8,
            "attack1": 7,
            "attack2": 8,
            "attack3": 11,
            "hurt": 4,
            "death": 4
        },
        "attacks": {
            "attack1": {
                "frames": [4, 5],
                "hitbox": {
                    "width": 80,
                    "height": 30,
                    "offset_x": 70,
                    "offset_y": 0
                }
            },
            "attack2": {
                "frames": [5, 6],
                "hitbox": {
                    "width": 60,
                    "height": 100,
                    "offset_x": 50,
                    "offset_y": -5
                }
            },
            "attack3": {
                "frames": [3, 7, 8],
                "hitbox": {
                    "width": 70,
                    "height": 120,
                    "offset_x": 65,
                    "offset_y": -5
                }
            }
        }
    },
    "axeman": {
        "name": "Axeman",
        "description": "High damage dealer",
        "folder": "axeman",
        "hp": 80,
        "speed": 12,
        "damage": 30,
        "animations_frames": {
            "idle": 6,
            "run": 8,
            "attack1": 9,
            "attack2": 9,
            "attack3": 12,
            "hurt": 4,
            "death": 4
        },
        "attacks": {
            "attack1": {
                "frames": [4, 5],
                "hitbox": {
                    "width": 70,
                    "height": 100,
                    "offset_x": 60,
                    "offset_y": -10
                }
            },
            "attack2": {
                "frames": [4, 5, 8],
                "hitbox": {
                    "width": 70,
                    "height": 90,
                    "offset_x": 65,
                    "offset_y": -10
                }
            },
            "attack3": {
                "frames": [4, 7, 8],
                "hitbox": {
                    "width": 80,
                    "height": 120,
                    "offset_x": 70,
                    "offset_y": -15
                }
            }
        }
    }
}

ENEMIES = {
    "orc": {
        "folder": "orc",
        "hp": 50,
        "damage": 5,
        "animations_frames": {
            "idle": 6,
            "run": 8,
            "attack1": 6,
            "attack2": 6,
            "hurt": 4,
            "death": 4
        },
        "attacks": {
            "attack1": {
                "frames": [3],
                "hitbox": {
                    "width": 50,
                    "height": 80,
                    "offset_x": 50,
                    "offset_y": -10
                }
            },
            "attack2": {
                "frames": [3],
                "hitbox": {
                    "width": 60,
                    "height": 90,
                    "offset_x": 55,
                    "offset_y": -15
                }
            }
        }
    },
    "armored_orc": {
        "folder": "armored_orc",
        "hp": 80,
        "damage": 8,
        "animations_frames": {
            "idle": 6,
            "run": 8,
            "attack1": 7,
            "attack2": 8,
            "hurt": 4,
            "death": 4
        },
        "attacks": {
            "attack1": {
                "frames": [4],
                "hitbox": {
                    "width": 60,
                    "height": 90,
                    "offset_x": 60,
                    "offset_y": -10
                }
            },
            "attack2": {
                "frames": [5],
                "hitbox": {
                    "width": 70,
                    "height": 100,
                    "offset_x": 65,
                    "offset_y": -15
                }
            }
        }
    },
    "skeleton": {
        "folder": "skeleton",
        "hp": 40,
        "damage": 6,
        "animations_frames": {
            "idle": 6,
            "run": 8,
            "attack1": 6,
            "attack2": 7,
            "hurt": 4,
            "death": 4
        },
        "attacks": {
            "attack1": {
                "frames": [3],
                "hitbox": {
                    "width": 50,
                    "height": 80,
                    "offset_x": 50,
                    "offset_y": -10
                }
            },
            "attack2": {
                "frames": [4],
                "hitbox": {
                    "width": 60,
                    "height": 90,
                    "offset_x": 55,
                    "offset_y": -15
                }
            }
        }
    },
    "armored_skeleton": {
        "folder": "armored_skeleton",
        "hp": 70,
        "damage": 9,
        "animations_frames": {
            "idle": 6,
            "run": 8,
            "attack1": 8,
            "attack2": 9,
            "hurt": 4,
            "death": 4
        },
        "attacks": {
            "attack1": {
                "frames": [4],
                "hitbox": {
                    "width": 60,
                    "height": 90,
                    "offset_x": 60,
                    "offset_y": -10
                }
            },
            "attack2": {
                "frames": [2, 6],
                "hitbox": {
                    "width": 70,
                    "height": 100,
                    "offset_x": 65,
                    "offset_y": -15
                }
            }
        }
    },
    "greatsword_skeleton": {
        "folder": "greatsword_skeleton",
        "hp": 90,
        "damage": 12,
        "animations_frames": {
            "idle": 6,
            "run": 9,
            "attack1": 9,
            "attack2": 12,
            "hurt": 4,
            "death": 4
        },
        "attacks": {
            "attack1": {
                "frames": [5, 6],
                "hitbox": {
                    "width": 80,
                    "height": 110,
                    "offset_x": 70,
                    "offset_y": -20
                }
            },
            "attack2": {
                "frames": [6, 7],
                "hitbox": {
                    "width": 90,
                    "height": 120,
                    "offset_x": 75,
                    "offset_y": -25
                }
            }
        }
    },
    "werewolf": {
        "folder": "werewolf",
        "hp": 100,
        "damage": 15,
        "animations_frames": {
            "idle": 6,
            "run": 8,
            "attack1": 9,
            "attack2": 13,
            "hurt": 4,
            "death": 4
        },
        "attacks": {
            "attack1": {
                "frames": [5, 6],
                "hitbox": {
                    "width": 70,
                    "height": 100,
                    "offset_x": 60,
                    "offset_y": -10
                }
            },
            "attack2": {
                "frames": [7, 8, 9, 10, 11],
                "hitbox": {
                    "width": 80,
                    "height": 110,
                    "offset_x": 65,
                    "offset_y": -15
                }
            }
        }
    },
    "werebear": {
        "folder": "werebear",
        "hp": 150,
        "damage": 20,
        "animations_frames": {
            "idle": 6,
            "run": 8,
            "attack1": 9,
            "attack2": 13,
            "hurt": 4,
            "death": 4
        },
        "attacks": {
            "attack1": {
                "frames": [5, 6],
                "hitbox": {
                    "width": 80,
                    "height": 110,
                    "offset_x": 70,
                    "offset_y": -10
                }
            },
            "attack2": {
                "frames": [4, 5, 9, 10],
                "hitbox": {
                    "width": 90,
                    "height": 120,
                    "offset_x": 75,
                    "offset_y": -15
                }
            }
        }
    }
}

ENEMY_SPEED = 3
NUMBER_OF_WAVES = 5

MAP_WIDTH = 8192
MAP_HEIGHT = 8192