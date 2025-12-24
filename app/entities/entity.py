import arcade

class Entity(arcade.Sprite):
    def __init__(self, image_path, scale, max_hp):
        super().__init__(image_path, scale)
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.speed = 0

    def take_damage(self, amount):
        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0
        # TODO: add color flashes for taking damage