import arcade
from app.entities.player import Player
from app.map.loader import load_game_map
from app.pve_logic.collision import PhysicsHandler

class PlayState(arcade.View):
    def __init__(self):
        super().__init__()
        # TODO: initialize Player, Map, PhysicsHandler, Spawner
        # TODO: setup main camera

    def on_show_view(self):
        pass

    def on_update(self, delta_time):
        # 1. Update Entities
        # 2. Update Physics (collisions with walls)
        # 3. Spawning logic (brain + spawning)
        # 4. Combat logic (collisions: player-enemy)
        # 5. Update Camera (center on player)
        pass

    def on_draw(self):
        arcade.start_render()
        self.camera_sprites.use()
        # TODO: draw the scene (map + entities)
        
        # UI Layer:
        # self.hud.draw(...)
        pass

    def on_key_press(self, key, modifiers):
        # TODO: pausing logic (ESC -> PauseState)
        pass