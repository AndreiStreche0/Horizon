import arcade

class GameMap:
    def __init__(self, tilemap: arcade.TileMap):
        self.tilemap = tilemap
        # Load everything from Tiled into Scene
        self.scene = arcade.Scene.from_tilemap(self.tilemap)

        # Dimensions
        self.width = tilemap.width * tilemap.tile_width
        self.height = tilemap.height * tilemap.tile_height

        collision_layer = self.scene.get_sprite_list("CollisionObject")
        
        if collision_layer:
            # If Walls does not already exist, add it as an alias for CollisionObject
            try:
                self.scene.get_sprite_list("Walls")
            except KeyError:
                self.scene.add_sprite_list("Walls", sprite_list=collision_layer)

    def get_walls(self):
        # Try to get Walls, if not, get CollisionObject, if not, empty list
        try:
            return self.scene.get_sprite_list("Walls")
        except KeyError:
            try:
                return self.scene.get_sprite_list("CollisionObject")
            except KeyError:
                return arcade.SpriteList()