import arcade

def load_game_map():
    scene = arcade.Scene()

    background_list = arcade.SpriteList()
    walls_list = arcade.SpriteList(use_spatial_hash=True)

    #basic green backround
    for x in range(0, 1200, 64):
        for y in range(0, 800, 64):
            sprite = arcade.SpriteSolidColor(64, 64, arcade.color.DARK_GREEN)
            sprite.center_x = x + 32
            sprite.center_y = y + 32
            background_list.append(sprite)

    for x in range(-32, 1232, 64):
        #simple top gray wall
        sprite = arcade.SpriteSolidColor(64, 64, arcade.color.GRAY)
        sprite.center_x = x
        sprite.center_y = 768
        walls_list.append(sprite)
        
        #simple bottom gray wall
        sprite = arcade.SpriteSolidColor(64, 64, arcade.color.GRAY)
        sprite.center_x = x
        sprite.center_y = 0
        walls_list.append(sprite)
    
    for y in range(0, 768, 64):
        #simple left gray wall
        sprite = arcade.SpriteSolidColor(64, 64, arcade.color.GRAY)
        sprite.center_x = 0
        sprite.center_y = y
        walls_list.append(sprite)
        
        #simple right gray wall
        sprite = arcade.SpriteSolidColor(64, 64, arcade.color.GRAY)
        sprite.center_x = 1024
        sprite.center_y = y
        walls_list.append(sprite)
    
    scene.add_sprite_list("Background", sprite_list=background_list)
    scene.add_sprite_list("Walls", sprite_list=walls_list)

    class SimpleTilemap:
        def __init__(self):
            self.scene = scene
            self.width = 1024
            self.height = 768
    
    return SimpleTilemap()