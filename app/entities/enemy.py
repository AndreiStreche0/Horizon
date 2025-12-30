import arcade
import math
import random
from pathlib import Path
from app.entities.entity import Entity
from config import ENEMY_SPEED, ENEMIES

BASE_DIR = Path(__file__).resolve().parents[2]

# Global cache: enemy_type -> {anim_name: [ {"right": Texture, "left": Texture}, ... ] }
ENEMY_TEXTURE_CACHE = {}

def _load_animation_frames(enemy_folder: str, animation_name: str, frame_count: int):
    """Load animation frames from disk and cache textures with flip variants."""
    textures = []
    folder = BASE_DIR / f"assets/enemies/{enemy_folder}/{animation_name}"
    for i in range(frame_count):
        texture_path = folder / f"{animation_name}_{i}.png"
        try:
            texture_right = arcade.load_texture(str(texture_path))
            texture_left = texture_right.flip_left_right()
            textures.append({"right": texture_right, "left": texture_left})
        except Exception as e:
            print(f"Warning: Could not load texture {texture_path}: {e}")
    return textures

def get_enemy_assets(enemy_type: str):
    """Get cached animation frames for enemy type, loading from disk only once per type."""
    if enemy_type in ENEMY_TEXTURE_CACHE:
        return ENEMY_TEXTURE_CACHE[enemy_type]
    
    data = ENEMIES[enemy_type]
    frames = data["animations_frames"]
    cache_entry = {
        "idle": _load_animation_frames(data["folder"], "idle", frames["idle"]),
        "run": _load_animation_frames(data["folder"], "run", frames["run"]),
        "attack1": _load_animation_frames(data["folder"], "attack1", frames["attack1"]),
        "attack2": _load_animation_frames(data["folder"], "attack2", frames["attack2"]),
        "hurt": _load_animation_frames(data["folder"], "hurt", frames["hurt"]),
        "death": _load_animation_frames(data["folder"], "death", frames["death"]),
    }
    ENEMY_TEXTURE_CACHE[enemy_type] = cache_entry
    return cache_entry

class Enemy(Entity):
    def __init__(self, x, y, level, enemy_list, enemy_type="orc"):
        self.enemy_type = enemy_type
        self.enemy_data = ENEMIES[enemy_type]

        assets = get_enemy_assets(enemy_type)
        initial_texture = assets["idle"][0]["right"] if assets["idle"] else None

        super().__init__(
            BASE_DIR / f"assets/enemies/{self.enemy_data['folder']}/idle/idle_0.png",
            1.0,
            self.enemy_data["hp"] + (level * 15)
        )
        
        if initial_texture:
            self.texture = initial_texture

        self.center_x = x
        self.center_y = y
        self.level = level

        self.speed = ENEMY_SPEED + (level * 0.1)
        self.damage = self.enemy_data["damage"] + (level * 2)
        self.xp_value = 10 + (level * 5)

        self.detection_range = 520
        self.attack_range = 50
        self.attack_cooldown = 1.5
        self.attack_timer = 0.0
        self.enemy_list = enemy_list

        self.wander_direction = random.uniform(0, 2 * math.pi)
        self.wander_timer = random.randint(30, 90)

        # --- Animation via cache ---
        self.idle_textures = assets["idle"]
        self.run_textures = assets["run"]
        self.attack1_textures = assets["attack1"]
        self.attack2_textures = assets["attack2"]
        self.hurt_textures = assets["hurt"]
        self.death_textures = assets["death"]

        self.current_texture = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.08
        self.death_hold_time = 0.0

        self.current_animation = "idle"
        self.facing_right = True
        self.is_attacking = False
        self.is_hurt = False
        self.is_dead = False
        self.animation_finished = False

        self.change_x = 0.0
        self.change_y = 0.0

        self.current_attack_type = 1

    def update_animation(self, delta_time: float = 0.0):
        if self.is_dead:
            if self.current_animation != "death":
                self.current_animation = "death"
                self.current_texture = 0
                self.animation_finished = False
        elif self.is_hurt:
            if self.current_animation != "hurt":
                self.current_animation = "hurt"
                self.current_texture = 0
                self.animation_finished = False
        elif self.is_attacking:
            pass
        elif self.change_x != 0 or self.change_y != 0:
            if self.current_animation != "run":
                self.current_animation = "run"
                self.current_texture = 0
        else:
            if self.current_animation != "idle" and not self.is_attacking:
                self.current_animation = "idle"
                self.current_texture = 0

        # Update facing direction based on movement
        if self.change_x < 0:
            self.facing_right = False
        elif self.change_x > 0:
            self.facing_right = True

        # Animate textures
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0

            if self.current_animation == "idle":
                textures = self.idle_textures
            elif self.current_animation == "run":
                textures = self.run_textures
            elif self.current_animation == "attack1":
                textures = self.attack1_textures
            elif self.current_animation == "attack2":
                textures = self.attack2_textures
            elif self.current_animation == "hurt":
                textures = self.hurt_textures
            elif self.current_animation == "death":
                textures = self.death_textures
            else:
                textures = self.idle_textures

            if textures:
                if self.current_animation == "death":
                    if self.current_texture < len(textures) - 1:
                        self.current_texture += 1
                        if self.current_texture == len(textures) - 1:
                            self.animation_finished = True
                    else:
                        self.animation_finished = True
                else:
                    self.current_texture = (self.current_texture + 1) % len(textures)

                    if self.current_texture == 0:
                        self.animation_finished = True
                        if self.is_hurt:
                            self.is_hurt = False
                        if self.is_attacking:
                            self.is_attacking = False

                if self.facing_right:
                    self.texture = textures[self.current_texture]["right"]
                else:
                    self.texture = textures[self.current_texture]["left"]
        
        if self.is_dead and self.current_texture >= len(self.death_textures) - 1:
            self.death_hold_time = max(0.0, self.death_hold_time - delta_time)

    def attack(self, attack_type=1):
        if not self.is_attacking and not self.is_hurt and not self.is_dead:
            self.is_attacking = True
            self.animation_finished = False
            self.current_attack_type = attack_type

            if attack_type == 1:
                self.current_animation = "attack1"
            elif attack_type == 2:
                self.current_animation = "attack2"

            self.current_texture = 0

    def take_damage(self, damage):
        if not self.is_dead:
            self.current_hp -= damage
            if self.current_hp <= 0:
                self.current_hp = 0
                self.die()
            else:
                self.is_hurt = True
                self.animation_finished = False
                self.current_animation = "hurt"
                self.current_texture = 0

    def die(self):
        self.is_dead = True
        self.current_animation = "death"
        self.current_texture = 0
        self.animation_finished = False
        self.change_x = 0.0
        self.change_y = 0.0
        self.death_hold_time = 1.0

    def update(self, delta_time, player_sprite):
        self.update_animation(delta_time)

        if self.is_dead:
            return False

        if self.attack_timer > 0:
            self.attack_timer -= delta_time

        # Calculate distance to player
        dx = player_sprite.center_x - self.center_x
        dy = player_sprite.center_y - self.center_y
        distance = math.hypot(dx, dy)

        self.change_x = 0.0
        self.change_y = 0.0

        should_attack = False

        # Don't move if attacking or hurt
        if not self.is_attacking and not self.is_hurt:
            if distance < self.detection_range:
                if distance > 0:
                    self.change_x = (dx / distance) * self.speed
                    self.change_y = (dy / distance) * self.speed

                if distance < self.attack_range:
                    if self.attack_timer <= 0:
                        self.attack_timer = self.attack_cooldown
                        # Randomly choose attack type
                        attack_type = random.choice([1, 2])
                        self.attack(attack_type)
                        should_attack = True
            else:
                # Wander behavior
                self.wander_timer -= 1
                if self.wander_timer <= 0:
                    self.wander_direction = random.uniform(0, 2 * math.pi)
                    self.wander_timer = random.randint(30, 90)

                self.change_x = math.cos(self.wander_direction) * self.speed * 0.5
                self.change_y = math.sin(self.wander_direction) * self.speed * 0.5

            # Separation logic so enemies don't stack on each other
            separation_x = 0.0
            separation_y = 0.0
            count = 0
            min_dist = 40

            for other in self.enemy_list:
                if other != self:
                    dist_x = self.center_x - other.center_x
                    dist_y = self.center_y - other.center_y
                    dist = math.hypot(dist_x, dist_y)

                    if dist < min_dist and dist > 0:
                        separation_x += (dist_x / dist) / dist
                        separation_y += (dist_y / dist) / dist
                        count += 1

            if count > 0:
                self.change_x += separation_x * 150
                self.change_y += separation_y * 150

        # Update position
        if not self.is_attacking and not self.is_hurt:
            self.center_x += self.change_x * delta_time
            self.center_y += self.change_y * delta_time

        return should_attack