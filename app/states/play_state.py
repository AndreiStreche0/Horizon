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

        # --- Player (will be initialized when showing view) ---
        self.player = None
        
        # --- Input tracking ---
        self.key_left = False
        self.key_right = False
        self.key_up = False
        self.key_down = False

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        
        # Create player with selected character
        character = getattr(self.brain, 'selected_character', 'knight')
        self.player = Player(character)
        self.player.center_x = 400
        self.player.center_y = 300
        
        # Clear and repopulate player list
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

    def on_update(self, delta_time):
        if self.player:
            # Update player movement based on keys
            self.player.update_movement(self.key_left, self.key_right, self.key_up, self.key_down)
            
            # Update positions and animation
            self.player_list.update(delta_time)

            # Verifică dacă player-ul e mort și animația s-a terminat
            if self.player.is_dead and self.player.animation_finished:
                self.brain.set_state("MENU")

    def on_draw(self):
        self.clear()

        self.camera_sprites.use()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.brain.set_state("MENU")

        # Movement keys
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.key_left = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_right = True
        elif key == arcade.key.UP or key == arcade.key.W:
            self.key_up = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.key_down = True

        # Attack keys
        elif key == arcade.key.Z:
            if self.player:
                self.player.attack(1)
        elif key == arcade.key.X:
            if self.player:
                self.player.attack(2)
        elif key == arcade.key.C:
            if self.player:
                self.player.attack(3)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.key_left = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.key_right = False
        elif key == arcade.key.UP or key == arcade.key.W:
            self.key_up = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.key_down = False