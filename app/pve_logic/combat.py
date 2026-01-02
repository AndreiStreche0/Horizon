import random
import time
import arcade

class CombatSystem:
    def __init__(self):
        self.player_attack_cooldown = 0.5
        self.player_last_attack_time = 0
        self.attack_range = 80
    def calculate_damage(self, attacker_level, base_dmg):
        damage = base_dmg + (attacker_level * 2)
        damage *= random.uniform(0.85, 1.15)
        return damage

    def player_can_attack(self):
        current_time = time.time()
        return current_time - self.player_last_attack_time > self.player_attack_cooldown

    def process_attack(self, player, enemies_list, physics_handler):
        if not self.player_can_attack():
            return [], 0
        current_time = time.time()
        self.player_last_attack_time = current_time
        max_range_attack = 0
        dead_targets = []
        for enemy in enemies_list:
            dx = player.center_x - enemy.center_x
            dy = player.center_y - enemy.center_y
            distance = (dx**2 + dy**2) ** 0.5
            if distance > max_range_attack:
                max_range_attack = distance
            if distance < self.attack_range:
                damage = self.calculate_damage(player.level, player.base_damage)
                if enemy.take_damage(damage):
                    dead_targets.append(enemy)
        return dead_targets, max_range_attack
    
    def enemy_attack_player(self, enemy, player):
        damage = self.calculate_damage(player.level, enemy.damage)
        player.take_damage(damage)
        return damage
    
    def calculate_xp_gain(self, enemy_level, player_level):
        base_xp = 10
        xp = base_xp + (enemy_level * 5)
        
        level_diff = player_level - enemy_level
        if level_diff > 3:
            xp = max(1, xp // (level_diff - 2))
        xp *= random.uniform(0.85, 1.15)
        return xp
    
    #TODO maybe improve logic, and add some feedback for UI
    def check_level_up(self, player):
        xp_needed = 100 * player.level
        
        if player.xp >= xp_needed:
            player.xp -= xp_needed
            return True
        return False