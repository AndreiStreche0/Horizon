import random
import time
import arcade
from app.entities.enemy import Enemy
from config import NUMBER_OF_WAVES, ENEMIES

class Spawner:
    def __init__(self, map_width, map_height, player_ref, base_spawn_interval, play_state):
        self.last_spawn_time = time.time()
        self.map_width = map_width
        self.map_height = map_height
        self.player_ref = player_ref
        self.base_spawn_interval = base_spawn_interval
        self.spawn_interval = base_spawn_interval
        self.play_state = play_state

        self.wave = 1
        self.enemies_per_wave = 5
        self.enemies_curr_wave = 0
        self.max_enemies = 35
        
        self.enemy_types = list(ENEMIES.keys())

    def should_spawn(self, enemy_cnt):
        current_time = time.time()
        if current_time - self.last_spawn_time < self.spawn_interval:
            return False
            
        if enemy_cnt >= self.max_enemies:
            return False
        
        if self.wave > NUMBER_OF_WAVES:
            return False

        if self.enemies_curr_wave >= self.enemies_per_wave:
            self.start_next_wave()
            return False
            
        return True

    def start_next_wave(self):
        self.wave += 1
        self.enemies_curr_wave = 0
        if self.wave == NUMBER_OF_WAVES:
            self.enemies_per_wave *= 2
        else:   
            self.enemies_per_wave += 3
       
        self.spawn_interval = max(1, self.base_spawn_interval - (self.wave * 0.1))
    
    def get_spawn_coordinates(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        padding = 50
        
        if side == 'top':
            x = random.randint(padding, self.map_width - padding)
            y = self.map_height + padding
        elif side == 'bottom':
            x = random.randint(padding, self.map_width - padding)
            y = -padding
        elif side == 'left':
            x = -padding
            y = random.randint(padding, self.map_height - padding)
        else:
            x = self.map_width + padding
            y = random.randint(padding, self.map_height - padding)
            
        return x, y
    
    def spawn_enemy(self, enemy_list):
        x, y = self.get_spawn_coordinates()
        
        enemy_level = min(self.wave // 3 + 1, 10)
        
        enemy_type = random.choice(self.enemy_types)
        
        enemy = Enemy(x, y, enemy_level, self.play_state.enemy_list, enemy_type=enemy_type)
        enemy_list.append(enemy)

        self.play_state.entity_list.append(enemy)
        self.last_spawn_time = time.time()
        self.enemies_curr_wave += 1
        self.play_state.physics_handler.add_enemy_hitbox(enemy)

        return enemy
    
    def update(self, delta_time, enemy_list):
        if self.should_spawn(len(enemy_list)):
            self.spawn_enemy(enemy_list)

    def get_wave_info(self):
        return {
            'wave': self.wave,
            'enemies_remaining': self.enemies_per_wave - self.enemies_curr_wave,
            'total_enemies': self.enemies_per_wave
        }