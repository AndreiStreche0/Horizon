import arcade
import math
import random
from config import ENEMY_SPEED

class Entity(arcade.Sprite):
    def __init__(self, image_path, scale, max_hp):
        super().__init__(image_path, scale)
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
        self.hit_flash_timer = self.hit_flash_duration
        #red flash
        self.color = (255, 100, 100)
        
        return self.current_hp <= 0

    def update_flash_animation(self, delta_time):
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= delta_time
            if self.hit_flash_timer <= 0:
                self.color = (255, 255, 255)