import random
import time
import arcade
import math
from config import PLAYABLE_CHARACTERS, ENEMIES
from arcade.geometry import are_polygons_intersecting

class CombatSystem:
    def __init__(self):
        self.player_attack_cooldown = 0.5
        self.player_last_attack_time = 0
        self.player_last_damage_frame = {}
        self.enemy_last_damage_frame = {}
        self.current_player_attack_id = 0
        
    def calculate_damage(self, attacker_level, base_dmg):
        damage = base_dmg + (attacker_level * 2)
        damage *= random.uniform(0.85, 1.15)
        return int(damage)

    def get_attack_hitbox(self, attacker, attack_type):
        if not attacker.is_attacking:
            return None

        if hasattr(attacker, 'character_type'):
            config = PLAYABLE_CHARACTERS[attacker.character_type]
        elif hasattr(attacker, 'enemy_type'):
            config = ENEMIES[attacker.enemy_type]
        else:
            return None
        
        attack_key = f"attack{attack_type}"
        if attack_key not in config.get("attacks", {}):
            return None
            
        attack_config = config["attacks"][attack_key]
        damage_frames = attack_config["frames"]
        
        if attacker.current_texture not in damage_frames:
            return None

        hitbox_config = attack_config["hitbox"]
        width = hitbox_config["width"]
        height = hitbox_config.get("height", hitbox_config.get("height:", 100))
        offset_x = hitbox_config["offset_x"]
        offset_y = hitbox_config["offset_y"]

        if attacker.facing_right:
            center_x = attacker.center_x + offset_x
        else:
            center_x = attacker.center_x - offset_x
            
        center_y = attacker.center_y + offset_y
        
        return (center_x, center_y, width, height)
    
    def check_hitbox_collision(self, hitbox, target):
        if hitbox is None:
            return False

        hb_center_x, hb_center_y, hb_width, hb_height = hitbox

        # Build attacker hitbox polygon in world coords (axis-aligned rect)
        hb_left = hb_center_x - hb_width / 2
        hb_right = hb_center_x + hb_width / 2
        hb_bottom = hb_center_y - hb_height / 2
        hb_top = hb_center_y + hb_height / 2
        attack_poly = [
            (hb_left, hb_bottom),
            (hb_right, hb_bottom),
            (hb_right, hb_top),
            (hb_left, hb_top),
        ]

        # Build target polygon using the entity’s custom hit box points if available
        target_poly = None

        # Preferred: entity-local points stored in Entity
        if hasattr(target, "_set_hit_box") and target._set_hit_box:
            target_poly = [(target.center_x + px, target.center_y + py)
                           for (px, py) in target._set_hit_box]

        if target_poly is None and hasattr(target, "get_adjusted_hit_box"):
            try:
                target_poly = target.get_adjusted_hit_box()
            except Exception:
                target_poly = None

        if target_poly is None:
            target_left = target.center_x - target.width / 2
            target_right = target.center_x + target.width / 2
            target_bottom = target.center_y - target.height / 2
            target_top = target.center_y + target.height / 2
            target_poly = [
                (target_left, target_bottom),
                (target_right, target_bottom),
                (target_right, target_top),
                (target_left, target_top),
            ]

        try:
            return are_polygons_intersecting(attack_poly, target_poly)
        except Exception:
            ax = [p[0] for p in attack_poly]
            ay = [p[1] for p in attack_poly]
            tx = [p[0] for p in target_poly]
            ty = [p[1] for p in target_poly]
            a_left, a_right = min(ax), max(ax)
            a_bottom, a_top = min(ay), max(ay)
            t_left, t_right = min(tx), max(tx)
            t_bottom, t_top = min(ty), max(ty)

            return not (a_right < t_left or
                        a_left > t_right or
                        a_top < t_bottom or
                        a_bottom > t_top)

    def player_can_attack(self):
        current_time = time.time()
        return current_time - self.player_last_attack_time > self.player_attack_cooldown

    def process_player_attack(self, player, enemies_list, attack_type):
        if not player.is_attacking:
            return []
        
        if player.is_hurt or player.is_dead:
            return []
        
        hitbox = self.get_attack_hitbox(player, attack_type)
        if hitbox is None:
            return []
        
        damaged_enemies = []
        current_frame = player.current_texture
        
        for enemy in enemies_list:
            if enemy.is_hurt or enemy.is_dead:
                continue
            
            enemy_id = id(enemy)
            
            if enemy_id in self.player_last_damage_frame:
                last_attack_id, last_frame = self.player_last_damage_frame[enemy_id]
                if last_attack_id == self.current_player_attack_id and last_frame == current_frame:
                    continue
            
            if self.check_hitbox_collision(hitbox, enemy):
                damage = self.calculate_damage(player.level, player.damage)
                
                dx = enemy.center_x - player.center_x
                dy = enemy.center_y - player.center_y
                distance = math.sqrt(dx * dx + dy * dy)
                
                enemy.take_damage(damage)
                
                self.player_last_damage_frame[enemy_id] = (self.current_player_attack_id, current_frame)
                damaged_enemies.append(enemy)
        
        return damaged_enemies
    
    def process_enemy_attack(self, enemy, player, attack_type):
        if not enemy.is_attacking:
            return False

        if enemy.is_hurt or enemy.is_dead:
            return False

        if player.is_dead:
            return False
        
        if player.is_hurt:
            return False
            
        hitbox = self.get_attack_hitbox(enemy, attack_type)
        if hitbox is None:
            return False
        
        enemy_id = id(enemy)
        current_frame = enemy.current_texture
        

        if enemy_id in self.enemy_last_damage_frame:
            last_attack_id, last_frame = self.enemy_last_damage_frame[enemy_id]

            attack_id = (enemy_id, enemy.current_animation)
            if last_attack_id == attack_id and last_frame == current_frame:
                return False

        if self.check_hitbox_collision(hitbox, player):
            damage = self.calculate_damage(enemy.level, enemy.damage)
            player.take_damage(damage)

            attack_id = (enemy_id, enemy.current_animation)
            self.enemy_last_damage_frame[enemy_id] = (attack_id, current_frame)
            return True
        
        return False
    
    def on_player_attack_start(self):
        self.current_player_attack_id += 1

        self.player_last_damage_frame = {
            k: v for k, v in self.player_last_damage_frame.items() 
            if v[0] >= self.current_player_attack_id - 1
        }
    
    def on_enemy_attack_start(self, enemy):
        enemy_id = id(enemy)
        if enemy_id in self.enemy_last_damage_frame:
            del self.enemy_last_damage_frame[enemy_id]
    
    def check_level_up(self, player):
        xp_needed = player.level * 100
        if player.xp >= xp_needed:
            player.xp -= xp_needed
            return True
        return False
    
    def calculate_xp_gain(self, enemy_level, player_level):
        base_xp = 10
        xp = base_xp + (enemy_level * 5)
        
        level_diff = player_level - enemy_level
        if level_diff > 3:
            xp = max(1, xp // (level_diff - 2))
        xp *= random.uniform(0.85, 1.15)
        return int(xp)