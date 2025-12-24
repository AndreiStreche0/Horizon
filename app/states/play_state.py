import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from app.entities.player import Player
from app.map.loader import load_game_map
from app.pve_logic.collision import PhysicsHandler
from app.ui.hud import HUD

class PlayState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        #initializing player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.player_list.append(self.player)

        #loading map
        self.tilemap = load_game_map()
        self.scene = self.tilemap.scene

        #loading walls
        self.wall_list = self.scene.get_sprite_list("Walls")

        #initializing physics logic
        self.physics_handler = PhysicsHandler(self.player, self.wall_list)
        self.brain.physics_handler = self.physics_handler

        #initializing HUD
        self.hud = HUD()
        self.brain.hud = self.hud

        #seting up camera
        self.camera_sprites = arcade.camera.Camera2D()
        self.camera_gui = arcade.camera.Camera2D()

        #keeping track of input
        self.keys_pressed = set()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_PASTEL_RED)
        self.brain.is_paused = False
        pass

    def on_update(self, delta_time):
        if self.brain.is_paused:
            return
        
        self.brain.game_time += delta_time
        self.player.update_movement()
        self.physics_handler.update()
        for enemy in self.enemy_list:
            enemy.update(delta_time, self.player)

        self.player.update_animation()
        self.center_camera_to_player()

    def center_camera_to_player(self):
        target_position = (self.player.center_x, self.player.center_y)
        
        self.camera_sprites.position = arcade.math.lerp_2d(
            self.camera_sprites.position, 
            target_position, 
            0.1
        )

    def on_draw(self):
        self.clear()
        
        self.camera_sprites.use()
        self.scene.draw()
        
        self.player_list.draw()
        self.enemy_list.draw()
        
        self.camera_gui.use()
        self.hud.draw(self.player, self.brain.score)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        
        # Player movement
        if key == arcade.key.W or key == arcade.key.UP:
            self.player.up_pressed = True
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player.down_pressed = True
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player.left_pressed = True
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.right_pressed = True
        # Game control
        elif key == arcade.key.ESCAPE:
            self.brain.set_state("PAUSE")
        elif key == arcade.key.SPACE:
            # TODO: Implement attack logic
            return
    
    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

        if key == arcade.key.W or key == arcade.key.UP:
            self.player.up_pressed = False
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player.down_pressed = False
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player.left_pressed = False
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.right_pressed = False