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
        self.player_engine.update()
        
        for enemy, engine in list(self.enemy_engines.items()):
            if enemy.current_hp <= 0: 
                continue
            engine.update()