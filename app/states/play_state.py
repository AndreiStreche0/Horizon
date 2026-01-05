import arcade
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, NUMBER_OF_WAVES
from app.entities.player import Player
from app.map.loader import load_game_map
from app.pve_logic.collision import PhysicsHandler
from app.pve_logic.combat import CombatSystem
from app.pve_logic.spawning import Spawner
from app.ui.hud import HUD
from app.achievements.achievement import AchievementTier

class PlayState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.entity_list = arcade.SpriteList()
        #initializing player
        character = getattr(self.brain, 'selected_character', 'knight')
        self.player = Player(character)
        self.player.center_x = 2500
        self.player.center_y = 7500
        self.player_list.append(self.player)
        self.entity_list.append(self.player)

        #loading map
        if self.brain.current_map is None:
            self.brain.current_map = load_game_map()
        self.tilemap = self.brain.current_map
        self.scene = self.tilemap.scene

        #loading walls
        self.wall_list = self.tilemap.get_walls()

        #initializing physics logic
        self.physics_handler = PhysicsHandler(self.player, self.wall_list)

        #combat and spawner logic
        self.combat_system = CombatSystem()

        self.spawner = Spawner(self.tilemap.width, self.tilemap.height, self.player, 10, self)
        #initializing HUD
        self.hud = HUD()
        self.brain.hud = self.hud

        #seting up camera
        self.camera_sprites = arcade.camera.Camera2D()
        self.camera_gui = arcade.camera.Camera2D()

        #keeping track of input
        self.keys_pressed = set()

        self.game_over = False
        self.wave_info = self.spawner.get_wave_info()
        self.current_attack_kills = 0
        self.session_enemies_killed = 0
        self.last_wave = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_PASTEL_RED)
        self.brain.is_paused = False
        pass

    def on_update(self, delta_time):
        if self.brain.is_paused or self.game_over:
            return
        
        self.brain.game_time += delta_time
        self.player.update_movement()
        self.physics_handler.update()
        self.player_list.update(delta_time)
        self.player_list.update_animation(delta_time)

        if self.player.is_dead and self.player.animation_finished and self.player.death_hold_time <= 0:
            self.game_over = True

        dead_enemies = []
        for enemy in self.enemy_list:
            was_attacking = enemy.is_attacking
            
            can_attack = enemy.update(delta_time, self.player)
            
            if enemy.is_attacking and not was_attacking:
                self.combat_system.on_enemy_attack_start(enemy)
            
            if enemy.is_attacking:
                hit_player = self.combat_system.process_enemy_attack(
                    enemy, self.player, enemy.current_attack_type
                )

            if enemy.is_dead and enemy.animation_finished and enemy.death_hold_time <= 0:
                dead_enemies.append(enemy)

        if self.player.is_attacking:
            damaged = self.combat_system.process_player_attack(
                self.player, self.enemy_list, self.player.current_attack_type
            )
            for enemy in damaged:
                if enemy.current_hp <= 0:
                    self.current_attack_kills += 1
        else:
            if self.current_attack_kills > 0:
                self.check_killtacular_achievement(self.current_attack_kills)
                self.current_attack_kills = 0

        for enemy in dead_enemies:
            xp_gained = self.combat_system.calculate_xp_gain(enemy.level, self.player.level)
            self.player.xp += xp_gained
            self.brain.score += xp_gained * 10 * random.uniform(0.85, 1.15)
            self.physics_handler.remove_enemy_hitbox(enemy)
            self.spawner.on_enemy_killed()

            dx = enemy.center_x - self.player.center_x
            dy = enemy.center_y - self.player.center_y
            distance = (dx * dx + dy * dy) ** 0.5
            self.check_sniper_achievement(distance)
            self.session_enemies_killed += 1
            self.brain.session_enemies_killed += 1

            self.enemy_list.remove(enemy)
            self.entity_list.remove(enemy)
            if self.player.is_attacking:
                self.current_attack_kills += 1

        self.enemy_list.update_animation()

        if self.combat_system.check_level_up(self.player):
            self.player.level_up()

        self.spawner.update(delta_time, self.enemy_list)
        self.wave_info = self.spawner.get_wave_info()

        if self.wave_info["wave"] > self.last_wave:
            if self.last_wave > 0:  # Not first wave
                self.player.reset_wave_damage()
            self.last_wave = self.wave_info["wave"]

        self.center_camera_to_player()
        self.brain.enemies = self.enemy_list

        if self.spawner.wave > NUMBER_OF_WAVES:
            is_high_score = self.brain.score > self.brain.high_score
            
            health_percent = (self.player.current_hp / self.player.max_hp) * 100
            self.check_barely_alive_achievement(health_percent)
            
            game_time_minutes = self.brain.game_time / 60.0
            self.check_speedrunner_achievement(game_time_minutes)

            self.check_flawless_victory_achievement(self.player.flawless_waves)

            self.brain.set_state("WIN", is_high_score)

    def center_camera_to_player(self):
        target_position = (self.player.center_x, self.player.center_y)
        
        self.camera_sprites.position = arcade.math.lerp_2d(
            self.camera_sprites.position, 
            target_position, 
            0.1
        )

    def on_draw(self):
        self.clear()
        
        self.camera_sprites.use()
        self.scene.draw()
        
        self.entity_list.sort(key=lambda sprite: -(sprite.center_y - sprite.height // 2))
        self.entity_list.draw()
        
        self.camera_gui.use()
        self.hud.draw(self.player, self.brain.score, self.wave_info, self.brain.game_time)
        if self.game_over:
            self.brain.set_state("LOSE")

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        
        # Player movement
        if key == arcade.key.W or key == arcade.key.UP:
            self.player.up_key = True
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player.down_key = True
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player.left_key = True
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.right_key = True
        # Game control
        elif key == arcade.key.ESCAPE:
            self.brain.set_state("PAUSE")
        elif key == arcade.key.Z:
            self.combat_system.on_player_attack_start()
            self.player.attack(1)
        elif key == arcade.key.X:
            self.combat_system.on_player_attack_start()
            self.player.attack(2)
        elif key == arcade.key.C:
            self.combat_system.on_player_attack_start()
            self.player.attack(3)
    
    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

        if key == arcade.key.W or key == arcade.key.UP:
            self.player.up_key = False
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player.down_key = False
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player.left_key = False
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.right_key = False

    def check_barely_alive_achievement(self, health_percent):
        achievement_name = "Barely Alive"
        username = self.brain.username

        if health_percent < 5:
            unlocked = self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.GOLD
            )
        elif health_percent < 10:
            unlocked = self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.SILVER
            )
        elif health_percent < 15:
            unlocked = self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.BRONZE
            )

    def check_killtacular_achievement(self, kills_count):
        achievement_name = "Killtacular"
        username = self.brain.username

        if kills_count >= 7:
            self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.GOLD
            )
        elif kills_count >= 5:
            self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.SILVER
            )
        elif kills_count >= 3:
            self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.BRONZE
            )

    def check_sniper_achievement(self, distance):
        achievement_name = "Sniper"
        username = self.brain.username

        if distance >= 80:
            self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.GOLD
            )
        elif distance >= 70:
            self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.SILVER
            )
        elif distance >= 60:
            self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.BRONZE
            )

    def check_speedrunner_achievement(self, minutes):
        achievement_name = "Speedrunner"
        username = self.brain.username

        if minutes <= 4:
            self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.GOLD
            )
        elif minutes <= 5:
            self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.SILVER
            )
        elif minutes <= 6:
            self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.BRONZE
            )

    def check_flawless_victory_achievement(self, flawless_waves):
        achievement_name = "Flawless Victory"
        username = self.brain.username

        if flawless_waves >= 5:
            self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.GOLD
            )
        elif flawless_waves >= 3:
            self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.SILVER
            )
        elif flawless_waves >= 2:
            self.brain.achievement_manager.unlock_achievement(
                username, achievement_name, AchievementTier.BRONZE
            )