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

class Enemy(Entity):
    def __init__(self, start_pos, level):
        # TODO: call super().__init__ with enemy asset
        # TODO: add enemy stats
        pass

    def follow_target(self, target_sprite):
        # TODO: calc the angle towars target_sprite (Player)
        # TODO: calc change_x change_y
        pass