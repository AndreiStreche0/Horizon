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

        self._set_hit_box = ([
            (-40, -30),
            (40, -30),
            (40, 30),
            (-40, 30)
        ])

        self._apply_custom_hit_box(self._set_hit_box)

    def _apply_custom_hit_box(self, points):
        if hasattr(self, "set_hit_box"):
            try:
                self.set_hit_box(points)
                return
            except Exception:
                pass
        if hasattr(self, "set_hit_box_points"):
            try:
                self.set_hit_box_points(points)
                return
            except Exception:
                pass
        try:
            self.hit_box_points = points
        except Exception:
            pass

    def update(self):
        super().update()

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0