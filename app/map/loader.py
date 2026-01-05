import arcade
from pathlib import Path
from app.map.tilemap import GameMap

BASE_DIR = Path(__file__).resolve().parents[2]
MAP_PATH = BASE_DIR / "assets" / "map" / "WorldMap.tmx"

def load_game_map():
    # Options for the CollisionObject layer
    layer_options = {
        "CollisionObject": {"use_spatial_hash": True},
    }

    tilemap = arcade.load_tilemap(str(MAP_PATH), layer_options=layer_options)

    # Create GameMap
    return GameMap(tilemap)