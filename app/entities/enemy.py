import arcade
import math
import random
from app.entities.entity import Entity
from config import ENEMY_SPEED

class Enemy(Entity):
    def __init__(self, x, y, level, enemy_list):
        #change hp from here
        super().__init__(":resources:images/animated_characters/zombie/zombie_idle.png", 0.5, 75 + (level * 15))
        
        self.center_x = x
        self.center_y = y
        self.level = level
        
        self.speed = ENEMY_SPEED + (level * 0.1)
        self.damage = 5 + (level * 2)
        self.xp_value = 10 + (level * 5)

        self.detection_range = 520
        self.attack_range = 50
        self.attack_cooldown = 1.5
        self.attack_timer = 0
        self.enemy_list = enemy_list

        self.wander_direction = random.uniform(0, 2 * math.pi)
        self.wander_timer = random.randint(30, 90)

    def update(self, delta_time, player_sprite):
        self.update_flash_animation(delta_time)
        if self.attack_timer > 0:
            self.attack_timer -= delta_time

        #distance
        dx = player_sprite.center_x - self.center_x
        dy = player_sprite.center_y - self.center_y
        distance = math.sqrt(dx**2 + dy**2)
        
        self.change_x = 0
        self.change_y = 0
        
        should_attack = False

        if distance < self.detection_range:
            if distance > 0:
                self.change_x = (dx / distance) * self.speed
                self.change_y = (dy / distance) * self.speed
                
            if distance < self.attack_range:
                if self.attack_timer <= 0:
                    self.attack_timer = self.attack_cooldown
                    should_attack = True
        else:
            self.wander_timer -= 1
            if self.wander_timer <= 0:
                self.wander_direction = random.uniform(0, 2 * math.pi)
                self.wander_timer = random.randint(30, 90)
            
            self.change_x = math.cos(self.wander_direction) * self.speed * 0.5
            self.change_y = math.sin(self.wander_direction) * self.speed * 0.5

        #separation logic so enemies dont stack on eachother

        separation_x = 0
        separation_y = 0
        count = 0
        min_dist = 40

        for other in self.enemy_list:
            if other != self:
                dist_x = self.center_x - other.center_x
                dist_y = self.center_y - other.center_y
                dist = math.sqrt(dist_x**2 + dist_y**2)

                if dist < min_dist and dist > 0:
                    separation_x += (dist_x / dist) / dist
                    separation_y += (dist_y / dist) / dist
                    count += 1

        if count > 0:
            #TODO change if necessary
            self.change_x += separation_x * 150
            self.change_y += separation_y * 150
        
        return should_attack