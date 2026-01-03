import random
import time
import arcade
import math
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
        self.enemies_spawned_in_wave = 0
        self.enemies_killed_in_wave = 0
        self.max_enemies = 35
        
        self.enemy_types = list(ENEMIES.keys())
        
        # Spawn settings
        self.spawn_min_distance = 500
        self.spawn_max_distance = 600
        self.collision_check_distance = 100

    def should_spawn(self, enemy_cnt):
        current_time = time.time()
        
        # Check if all enemies in current wave are dead - advance immediately
        if self.enemies_killed_in_wave >= self.enemies_per_wave:
            self.start_next_wave()
            # Don't spawn immediately after wave change, respect cooldown
            if current_time - self.last_spawn_time < self.spawn_interval:
                return False
        
        if current_time - self.last_spawn_time < self.spawn_interval:
            return False
            
        # Restrict based on global max enemies
        if enemy_cnt >= self.max_enemies:
            return False
        
        if self.wave > NUMBER_OF_WAVES:
            return False

        # Check if we've already spawned all enemies for this wave
        if self.enemies_spawned_in_wave >= self.enemies_per_wave:
            return False
        
        # Calculate how many enemies can exist on map for current wave
        max_alive_in_wave = self.enemies_per_wave - self.enemies_killed_in_wave
        if enemy_cnt >= max_alive_in_wave:
            return False
            
        return True

    def start_next_wave(self):
        self.wave += 1
        self.enemies_spawned_in_wave = 0
        self.enemies_killed_in_wave = 0
        if self.wave == NUMBER_OF_WAVES:
            self.enemies_per_wave *= 2
        else:   
            self.enemies_per_wave += 3
       
        self.spawn_interval = max(1, self.base_spawn_interval - (self.wave * 1.5))
    
    def is_valid_spawn_position(self, x, y):
        # Distance from player
        dist_from_player = ((x - self.player_ref.center_x) ** 2 + (y - self.player_ref.center_y) ** 2) ** 0.5
        
        if dist_from_player < self.spawn_min_distance or dist_from_player > self.spawn_max_distance:
            return False
        
        # Verify collision with walls (wall_list)
        wall_list = self.play_state.wall_list
        for wall in wall_list:
            wall_dist = ((x - wall.center_x) ** 2 + (y - wall.center_y) ** 2) ** 0.5
            if wall_dist < self.collision_check_distance + wall.width / 2:
                return False
        
        return True
    
    def get_spawn_coordinates(self):
        max_attempts = 20
        
        for attempt in range(max_attempts):
            # Generate random position around player
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(self.spawn_min_distance, self.spawn_max_distance)
            
            x = self.player_ref.center_x + distance * math.cos(angle)
            y = self.player_ref.center_y + distance * math.sin(angle)
            
            # Clamp on map
            x = max(0, min(x, self.map_width))
            y = max(0, min(y, self.map_height))
            
            if self.is_valid_spawn_position(x, y):
                return x, y
        
        # Fallback: try map edges
        for attempt in range(max_attempts):
            side = random.choice(['top', 'bottom', 'left', 'right'])
            padding = 50
            
            if side == 'top':
                x = random.randint(padding, self.map_width - padding)
                y = self.map_height - padding
            elif side == 'bottom':
                x = random.randint(padding, self.map_width - padding)
                y = padding
            elif side == 'left':
                x = padding
                y = random.randint(padding, self.map_height - padding)
            else:
                x = self.map_width - padding
                y = random.randint(padding, self.map_height - padding)
            
            if self.is_valid_spawn_position(x, y):
                return x, y
        
        # Last fallback: random position on map
        return random.randint(50, self.map_width - 50), random.randint(50, self.map_height - 50)
    
    def spawn_enemy(self, enemy_list):
        x, y = self.get_spawn_coordinates()
        
        enemy_level = min(self.wave // 3 + 1, 10)
        enemy_type = random.choice(self.enemy_types)
        
        enemy = Enemy(x, y, enemy_level, self.play_state.enemy_list, enemy_type=enemy_type)
        enemy_list.append(enemy)
        self.play_state.entity_list.append(enemy)
        
        self.last_spawn_time = time.time()
        self.enemies_spawned_in_wave += 1
        self.play_state.physics_handler.add_enemy_hitbox(enemy)

        return enemy
    
    def on_enemy_killed(self):
        self.enemies_killed_in_wave += 1
    
    def update(self, delta_time, enemy_list):
        if self.should_spawn(len(enemy_list)):
            self.spawn_enemy(enemy_list)

    def get_wave_info(self):
        enemies_left_to_spawn = self.enemies_per_wave - self.enemies_killed_in_wave
        return {
            'wave': self.wave,
            'enemies_remaining': enemies_left_to_spawn,
            'total_enemies': self.enemies_per_wave
        }