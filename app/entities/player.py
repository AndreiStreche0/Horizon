from app.entities.entity import Entity
from config import PLAYER_SPEED, PLAYER_START_HP
import arcade

class Player(Entity):
    def __init__(self, x, y):
        #TODO: update it
        super().__init__(":resources:images/animated_characters/female_person/femalePerson_idle.png", 0.5, PLAYER_START_HP)
        #super().__init__("path/to/player.png", 1.0, 100)
        #initializing player
        self.center_x = x
        self.center_y = y
        self.speed = PLAYER_SPEED
        self.xp = 0
        self.level = 1

        #initializing movement
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
    def update_movement(self):
        self.change_x = 0
        self.change_y = 0
        
        if self.left_pressed and not self.right_pressed:
            self.change_x = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.change_x = self.speed
        if self.up_pressed and not self.down_pressed:
            self.change_y = self.speed
        if self.down_pressed and not self.up_pressed:
            self.change_y = -self.speed

    def level_up(self):
        # TODO: improve player stats
        pass