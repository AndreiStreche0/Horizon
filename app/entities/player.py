from app.entities.entity import Entity
import arcade
from pathlib import Path
from config import PLAYABLE_CHARACTERS

BASE_DIR = Path(__file__).resolve().parents[2]

class Player(Entity):
    def __init__(self, character_type="knight"):
        self.character_type = character_type
        self.character_data = PLAYABLE_CHARACTERS[character_type]
        
        # Entity(texture, scale, max_hp)
        super().__init__(BASE_DIR / f"assets/player/{self.character_data['folder']}/idle/idle_0.png", 1.0, self.character_data["hp"])

        # Player-specific stats from character data
        self.speed = self.character_data["speed"]
        self.damage = self.character_data["damage"]
        self.xp = 0
        self.level = 1
        
        self.left_key = False
        self.right_key = False
        self.up_key = False
        self.down_key = False

        # --- Animation ---
        self.idle_textures = []
        self.run_textures = []
        self.attack1_textures = []
        self.attack2_textures = []
        self.attack3_textures = []
        self.hurt_textures = []
        self.death_textures = []
        self.current_texture = 0
        self.animation_timer = 0
        self.animation_speed = 0.08
        self.death_hold_time = 0.0

        self.current_animation = "idle"
        self.facing_right = True
        self.is_attacking = False
        self.is_hurt = False
        self.is_dead = False
        self.animation_finished = False

        self.current_attack_type = 1

        self.load_animations()

        # Set initial texture
        self.texture = self.idle_textures[0]["right"]

    def load_animations(self):
        frames = self.character_data["animations_frames"]
        self.idle_textures = self.load_animation_frames("idle", frames["idle"])
        self.run_textures = self.load_animation_frames("run", frames["run"])
        self.attack1_textures = self.load_animation_frames("attack1", frames["attack1"])
        self.attack2_textures = self.load_animation_frames("attack2", frames["attack2"])
        self.attack3_textures = self.load_animation_frames("attack3", frames["attack3"])
        self.hurt_textures = self.load_animation_frames("hurt", frames["hurt"])
        self.death_textures = self.load_animation_frames("death", frames["death"])

    def load_animation_frames(self, animation_name, frame_count):
        folder = BASE_DIR / f"assets/player/{self.character_data['folder']}/{animation_name}"
        textures = []

        for i in range(frame_count):
            texture_path = folder / f"{animation_name}_{i}.png"

            texture_right = arcade.load_texture(str(texture_path))
            texture_left = texture_right.flip_left_right()

            textures.append({
                "right": texture_right,
                "left": texture_left
            })

        return textures

    def update(self, delta_time: float):
        if not self.is_dead:
            self.center_x += self.change_x * delta_time
            self.center_y += self.change_y * delta_time

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

        if self.change_x < 0:
            self.facing_right = False
        elif self.change_x > 0:
            self.facing_right = True

        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0

            if self.current_animation == "idle":
                textures = self.idle_textures
            elif self.current_animation == "run":
                textures = self.run_textures
            elif self.current_animation == "attack1":
                textures = self.attack1_textures
            elif self.current_animation == "attack2":
                textures = self.attack2_textures
            elif self.current_animation == "attack3":
                textures = self.attack3_textures
            elif self.current_animation == "hurt":
                textures = self.hurt_textures
            elif self.current_animation == "death":
                textures = self.death_textures
            else:
                textures = self.idle_textures

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

    def update_movement(self):
        if self.is_attacking or self.is_hurt or self.is_dead:
            self.change_x = 0
            self.change_y = 0
            return

        self.change_x = 0
        self.change_y = 0

        if self.left_key and not self.right_key:
            self.change_x = -self.speed
        if self.right_key and not self.left_key:
            self.change_x = self.speed
        if self.up_key and not self.down_key:
            self.change_y = self.speed
        if self.down_key and not self.up_key:
            self.change_y = -self.speed
        #diagonal movement
        if self.change_x != 0 and self.change_y != 0:
            self.change_x *= (2 ** 0.5)
            self.change_y *= (2 ** 0.5)

    def attack(self, attack_type):
        if not self.is_attacking and not self.is_hurt and not self.is_dead:
            self.is_attacking = True
            self.animation_finished = False
            self.change_x = 0
            self.change_y = 0
            self.current_attack_type = attack_type
            
            if attack_type == 1:
                self.current_animation = "attack1"
            elif attack_type == 2:
                self.current_animation = "attack2"
            elif attack_type == 3:
                self.current_animation = "attack3"
            
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
                self.change_x = 0
                self.change_y = 0
                self.current_animation = "hurt"
                self.current_texture = 0

    def die(self):
        self.is_dead = True
        self.animation_finished = False
        self.change_x = 0
        self.change_y = 0
        self.current_animation = "death"
        self.current_texture = 0
        self.death_hold_time = 1.0

    def level_up(self):
        #TODO add something for UI, a level up animation
        self.level += 1
        self.max_hp += self.level * 15
        self.current_hp = self.max_hp
        self.speed += 0.2
        self.damage += max(10, 2 * self.level)
        return self.level