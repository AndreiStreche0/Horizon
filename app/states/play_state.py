import arcade
from arcade.camera import Camera2D

from app.entities.player import Player
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class PlayState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain

        # --- Camera ---
        self.camera_sprites = Camera2D()

        # --- Sprite lists ---
        self.player_list = arcade.SpriteList()

        # --- Player ---
        self.player = Player()
        self.player.center_x = 400
        self.player.center_y = 300
        self.player_list.append(self.player)
        
        # --- Input tracking ---
        self.key_left = False
        self.key_right = False
        self.key_up = False
        self.key_down = False

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_update(self, delta_time):
        # Update player movement based on keys
        self.player.update_movement(self.key_left, self.key_right, self.key_up, self.key_down)
        
        # Update positions and animation
        self.player_list.update(delta_time)

    def on_draw(self):
        self.clear()

        self.camera_sprites.use()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.brain.set_state("MENU")
        
        # Movement keys - Arrow keys
        elif key == arcade.key.LEFT:
            self.key_left = True
        elif key == arcade.key.RIGHT:
            self.key_right = True
        elif key == arcade.key.UP:
            self.key_up = True
        elif key == arcade.key.DOWN:
            self.key_down = True
        
        # Movement keys - WASD
        elif key == arcade.key.A:
            self.key_left = True
        elif key == arcade.key.D:
            self.key_right = True
        elif key == arcade.key.W:
            self.key_up = True
        elif key == arcade.key.S:
            self.key_down = True

    def on_key_release(self, key, modifiers):
        # Arrow keys
        if key == arcade.key.LEFT:
            self.key_left = False
        elif key == arcade.key.RIGHT:
            self.key_right = False
        elif key == arcade.key.UP:
            self.key_up = False
        elif key == arcade.key.DOWN:
            self.key_down = False
        
        # WASD
        elif key == arcade.key.A:
            self.key_left = False
        elif key == arcade.key.D:
            self.key_right = False
        elif key == arcade.key.W:
            self.key_up = False
        elif key == arcade.key.S:
            self.key_down = False