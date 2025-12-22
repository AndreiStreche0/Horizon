import arcade

class PhysicsHandler:
    def __init__(self, player, wall_list):
        self.engine = arcade.PhysicsEngineSimple(player, wall_list)

    def update(self):
        self.engine.update()

    def check_enemy_collisions(self, player, enemies):
        # TODO: using arcade.check_for_collision_with_list return list of enemies touching the player
        pass