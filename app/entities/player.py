from app.entities.entity import Entity
import arcade

class Player(Entity):
    def __init__(self):
        #TODO: update it
        super().__init__("path/to/player.png", 1.0, 100)
        self.xp = 0
        self.level = 1

    def update_movement(self, key_left, key_right, key_up, key_down):
        # TODO: reset change_x/y to 0
        # TODO: change speed based on input
        pass

    def level_up(self):
        # TODO: improve player stats
        pass