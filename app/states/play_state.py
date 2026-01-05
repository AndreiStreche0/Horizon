import arcade
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, NUMBER_OF_WAVES
from app.entities.player import Player
from app.map.loader import load_game_map
from app.pve_logic.collision import PhysicsHandler
from app.pve_logic.combat import CombatSystem
from app.pve_logic.spawning import Spawner
from app.ui.hud import HUD
from storage.authentification import AuthentificationManager

class PlayState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.authentificator = AuthentificationManager()
        #initializing player
        character = getattr(self.brain, 'selected_character', 'knight')
        self.player = Player(character)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player)
        self.traveled_distance = 0
        self.tanked_damage = 0
        #loading map
        self.tilemap = load_game_map()
        self.scene = self.tilemap.scene

        #loading walls
        self.wall_list = self.scene.get_sprite_list("Walls")

        #initializing physics logic
        self.physics_handler = PhysicsHandler(self.player, self.wall_list)

        #combat and spawner logic
        self.combat_system = CombatSystem()
        #TODO: the spawning base interval can be changed here
        self.spawner = Spawner(self.tilemap.width, self.tilemap.height, self.player, 10, self)
        #initializing HUD
        self.hud = HUD()
        self.brain.hud = self.hud

        #seting up camera
        self.camera_sprites = arcade.camera.Camera2D()
        self.camera_gui = arcade.camera.Camera2D()

        #keeping track of input
        self.keys_pressed = set()
        self.current_wave_number = 1
        self.low_health_alert_timer = 0 
        self.showed_first_wave = False
        self.game_over = False
        self.wave_info = self.spawner.get_wave_info()
        #TODO add ui text : game started and maybe some basic instructions

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_PASTEL_RED)
        self.brain.is_paused = False
        pass

    def on_update(self, delta_time):
        if self.brain.is_paused or self.game_over:
            return
        
        self.brain.game_time += delta_time
        self.hud.update(delta_time)
        self.player.update_movement()
        self.physics_handler.update()
        self.player_list.update(delta_time)
        self.player_list.update_animation(delta_time)
        self.traveled_distance += (self.player.change_x**2 + self.player.change_y**2)**0.5
        dead_enemies = []
        past_hp = self.player.current_hp
        for enemy in self.enemy_list:
            can_attack = enemy.update(delta_time, self.player)
            
            if can_attack:
                self.combat_system.enemy_attack_player(enemy, self.player)

                if self.player.current_hp <= 0:
                    self.game_over = True
            
            if enemy.current_hp <= 0:
                dead_enemies.append(enemy)
        self.tanked_damage += (past_hp - self.player.current_hp)

        hp_percent = self.player.current_hp / self.player.max_hp
        if hp_percent < 0.10 and self.player.current_hp > 0:
            self.low_health_alert_timer -= delta_time
            if self.low_health_alert_timer <= 0:
                self.hud.add_message("LOW HEALTH!", arcade.color.RED, duration=1.0)
                self.low_health_alert_timer = 5.0

        for enemy in dead_enemies:
            xp_gained = self.combat_system.calculate_xp_gain(enemy.level, self.player.level)
            self.player.xp += xp_gained
            #TODO this logic could be improved
            self.brain.score += xp_gained * 10 * random.uniform(0.85, 1.15)

            #TODO maybe in a corner a small message can appear each time an enemy dies
            self.physics_handler.remove_enemy_hitbox(enemy)
            self.enemy_list.remove(enemy)

        self.enemy_list.update_animation()

        if self.combat_system.check_level_up(self.player):
            self.player.level_up()
        
        self.spawner.update(delta_time, self.enemy_list)
        self.wave_info = self.spawner.get_wave_info()

        self.center_camera_to_player()
        self.brain.enemies = self.enemy_list

        if (self.spawner.wave > self.current_wave_number or self.current_wave_number == 1 and self.showed_first_wave == False) and self.spawner.wave <= NUMBER_OF_WAVES:
            self.current_wave_number = self.spawner.wave
            self.showed_first_wave = True
            self.hud.add_message(f"WAVE {self.current_wave_number} STARTED!", arcade.color.PURPLE, duration=3.0)

        if self.spawner.wave > NUMBER_OF_WAVES and len(self.enemy_list) == 0:
            score_bonus = max(0, 2500 - (7 * self.brain.game_time))
            self.brain.score += score_bonus
            is_high_score = self.brain.score > self.brain.high_score
            self.brain.new_score(self.brain.score)
            #for Achievements
            self.brain.achievements.update("Game Veteran", self.brain.game_time / 3600.0)
            self.brain.achievements.update("Distance Traveled", self.traveled_distance)
            self.brain.achievements.update("Game Master", self.brain.score)
            self.brain.achievements.update("Barely Alive", self.player.current_hp)
            self.brain.achievements.update("Total Winner", 1)
            self.brain.achievements.update("Speed Runner", self.brain.game_time)
            self.brain.achievements.update("Super Tank", self.tanked_damage)

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
        
        self.player_list.draw()
        self.enemy_list.draw()
        
        self.camera_gui.use()
        self.hud.draw(self.player, self.brain.score, self.wave_info, self.brain.game_time)
        if self.game_over:
            #for Achievements
            self.brain.achievements.update("Game Veteran", self.brain.game_time / 3600.0)
            self.brain.achievements.update("Distance Traveled", self.traveled_distance)
            self.brain.achievements.update("Super Tank", self.tanked_damage)
            self.brain.set_state("LOSE")
    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        max_range = 0
        dead_cnt = 0
        dead_list = []
        #player movement
        if key == arcade.key.W or key == arcade.key.UP:
            self.player.up_key = True
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player.down_key = True
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.player.left_key = True
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.right_key = True
        #game control
        elif key == arcade.key.ESCAPE:
            self.brain.set_state("PAUSE")
        elif key == arcade.key.Z:
            self.player.attack(1)
            dead_list, max_range = self.combat_system.process_attack(self.player,self.enemy_list,self.physics_handler)
        elif key == arcade.key.X:
            self.player.attack(2)
            dead_list, max_range = self.combat_system.process_attack(self.player,self.enemy_list,self.physics_handler)
        elif key == arcade.key.C:
            self.player.attack(3)
            dead_list, max_range = self.combat_system.process_attack(self.player,self.enemy_list,self.physics_handler)
        if dead_list:
            dead_cnt = len(dead_list)
        #for Achievements
        if dead_cnt != 0:
            self.brain.achievements.update("Multi Kill", dead_cnt)
            self.brain.achievements.update("Total Killer", dead_cnt)
        if max_range != 0:
            self.brain.achievements.update("Sniper", max_range)

        if dead_cnt > 0:
            if dead_cnt == 1:
                self.hud.add_message("Enemy Slain", arcade.color.YELLOW, 0.75)
            elif dead_cnt == 2:
                self.hud.add_message("DOUBLE KILL!", arcade.color.DARK_YELLOW, 1.5)
            elif dead_cnt == 3:
                self.hud.add_message("TRIPLE KILL!", arcade.color.ORANGE, 2.25)
            elif dead_cnt == 4:
                self.hud.add_message("QUADRA KILL!", arcade.color.RED, 3.5)
            elif dead_cnt >= 5:
                self.hud.add_message("PENTA KILL!", arcade.color.VIOLET, 5)

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
