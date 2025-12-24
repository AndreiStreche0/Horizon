from app.entities.entity import Entity
import arcade
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class Player(Entity):
    def __init__(self):
        # Entity(texture, scale, hp)
        super().__init__(None, 1.0, 100)

        # Player-specific stats
        self.speed = 100
        self.xp = 0
        self.level = 1

        # --- Animation ---
        self.idle_textures = []
        self.run_textures = []
        self.current_texture = 0
        self.animation_timer = 0
        self.animation_speed = 0.15

        self.current_animation = "idle"
        self.facing_right = True

        self.load_animations()

        # Set initial texture
        self.texture = self.idle_textures[0]["right"]

    def load_animations(self):
        self.idle_textures = self.load_animation_frames("idle", 6)
        self.run_textures = self.load_animation_frames("run", 8)

    def load_animation_frames(self, animation_name, frame_count):
        folder = BASE_DIR / f"assets/player/knight/{animation_name}"
        textures = []

        for i in range(frame_count):
            texture_path = folder / f"{animation_name}_{i}.png"

            texture_right = arcade.load_texture(str(texture_path))
            texture_left = texture_right.flip_left_right()

            textures.append({
                "right": texture_right,
                "left": texture_left
            })

        return textures

    def update(self, delta_time: float):
        # Determină animația curentă
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        if self.change_x != 0 or self.change_y != 0:
            if self.current_animation != "run":
                self.current_animation = "run"
                self.current_texture = 0
        else:
            if self.current_animation != "idle":
                self.current_animation = "idle"
                self.current_texture = 0

        # Determină direcția
        if self.change_x < 0:
            self.facing_right = False
        elif self.change_x > 0:
            self.facing_right = True

        # Actualizează frame-ul animației
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            if self.current_animation == "idle":
                textures = self.idle_textures
            elif self.current_animation == "run":
                textures = self.run_textures
            else:
                textures = self.idle_textures

            self.current_texture = (self.current_texture + 1) % len(textures)

            if self.facing_right:
                self.texture = textures[self.current_texture]["right"]
            else:
                self.texture = textures[self.current_texture]["left"]

    def update_movement(self, key_left, key_right, key_up, key_down):
        self.change_x = 0
        self.change_y = 0

        if key_left:
            self.change_x = -self.speed
        elif key_right:
            self.change_x = self.speed

        if key_up:
            self.change_y = self.speed
        elif key_down:
            self.change_y = -self.speed

    def level_up(self):
        # TODO: improve player stats
        pass