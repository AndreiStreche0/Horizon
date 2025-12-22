import arcade

class GameMap:
    def __init__(self, tilemap_object):
        self.scene = arcade.Scene.from_tilemap(tilemap_object)
        # TODO: get map dimensions
        
    def get_walls(self):
        # TODO: return self.scene["Walls"]
        pass