import arcade

class PhysicsHandler:
    def __init__(self, player, wall_list):
        self.player = player
        self.wall_list = wall_list
        self.player_engine = arcade.PhysicsEngineSimple(player, wall_list)
        self.enemy_engines = {}

    def add_enemy_hitbox(self, enemy):
        engine = arcade.PhysicsEngineSimple(enemy, self.wall_list)
        self.enemy_engines[enemy] = engine

    def remove_enemy_hitbox(self, enemy):
        if enemy in self.enemy_engines:
            del self.enemy_engines[enemy]

    def update(self):
        # Save player position before update
        prev_x = self.player.center_x
        prev_y = self.player.center_y
        
        self.player_engine.update()
        
        distance = ((self.player.center_x - prev_x) ** 2 + (self.player.center_y - prev_y) ** 2) ** 0.5
        if distance > 100:
            self.player.center_x = prev_x
            self.player.center_y = prev_y
        
        for enemy, engine in list(self.enemy_engines.items()):
            if enemy.current_hp <= 0: 
                continue
            
            prev_enemy_x = enemy.center_x
            prev_enemy_y = enemy.center_y
            
            engine.update()
            
            distance = ((enemy.center_x - prev_enemy_x) ** 2 + (enemy.center_y - prev_enemy_y) ** 2) ** 0.5
            if distance > 100:
                enemy.center_x = prev_enemy_x
                enemy.center_y = prev_enemy_y