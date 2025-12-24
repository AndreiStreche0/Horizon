import random
import time
import arcade
from app.entities.enemy import Enemy

class Spawner:
    def __init__(self, map_width, map_height, player_ref, base_spawn_interval):
        self.last_spawn_time = time.time()
        self.map_width = map_width
        self.map_height = map_height
        self.player_ref = player_ref
        self.base_spawn_interval = base_spawn_interval
        self.spawn_interval = base_spawn_interval
        self.last_spawn_time = time.time()

        self.wave = 1
        self.enemies_per_wave = 5
        self.enemies_curr_wave = 0
        self.max_enemies = 20

    def should_spawn(self, enemy_cnt):
        current_time = time.time()
        
        if current_time - self.last_spawn_time < self.spawn_interval:
            return False
            
        if enemy_cnt >= self.max_enemies:
            return False
            
        if self.enemies_curr_wave >= self.enemies_per_wave:
            self.start_next_wave()
            return False
            
        return True

    def start_next_wave(self):
        self.wave += 1
        self.enemies_curr_wave = 0
        self.enemies_per_wave += 3

        #TODO change to better logic, maybe around current level        
        self.spawn_interval = max(1, self.base_spawn_interval - (self.wave * 0.1))
        
        #TODO maybe some text alerting a new wave starting

    def get_spawn_coordinates(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        padding = 50
        
        #random coords at map borders
        #TODO maybe change to better logic
        if side == 'top':
            x = random.randint(padding, self.map_width - padding)
            y = self.map_height + padding
        elif side == 'bottom':
            x = random.randint(padding, self.map_width - padding)
            y = -padding
        elif side == 'left':
            x = -padding
            y = random.randint(padding, self.map_height - padding)
        else:  # right
            x = self.map_width + padding
            y = random.randint(padding, self.map_height - padding)
            
        return x, y
    
    def spawn_enemy(self, enemy_list):
        x, y = self.get_spawn_coordinates()
        
        #TODO change level logic, maybe based on player level or another better logic
        enemy_level = min(self.wave // 3 + 1, 10)
        
        enemy = Enemy(x, y, enemy_level)
        enemy_list.append(enemy)
        
        self.last_spawn_time = time.time()
        self.enemies_curr_wave += 1
        
        return enemy
    
    def update(self, delta_time, enemy_list):
        if self.should_spawn(len(enemy_list)):
            self.spawn_enemy(enemy_list)

    def get_wave_info(self):
        #TODO use this in UI for the current wave and current progress
        return {
            'wave': self.wave,
            'enemies_remaining': self.enemies_per_wave - self.enemies_curr_wave,
            'total_enemies': self.enemies_per_wave
        }