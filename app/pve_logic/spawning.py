import random
import time

class Spawner:
    def __init__(self):
        self.last_spawn_time = time.time()

    def should_spawn(self, spawn_interval):
        # TODO: check time passed from last spawn or a different logic
        pass

    def get_spawn_coordinates(self, player_pos, screen_bounds):
        # TODO: generate random coordinates outside of screen bounds
        pass