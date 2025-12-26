import arcade
import math
import random
from config import ENEMY_SPEED

class Entity(arcade.Sprite):
    def __init__(self, image_path, scale, max_hp):
        if image_path:
            super().__init__(image_path, scale)
        else:
            super().__init__(scale=scale)
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.hit_flash_timer = 0
        self.hit_flash_duration = 0.2

    def update(self):
        super().update()

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0