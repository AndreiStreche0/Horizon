import arcade

#handles game state and current session
class Brain:
    def __init__(self, window):
        self.window = window
        
        self.score = 0
        self.current_level = 1
        #TODO change this when sttorage is implemented
        self.high_score = 0
        self.username = "Player"
        self.game_time = 0
        self.is_paused = False
        #TODO change so this is dependant on character choice
        self.player_base_damage = 20

        self.player = None
        self.enemies = []
        self.current_map = None
        self.spawner = None
        self.physics_handler = None
        self.hud = None

    def set_state(self, state_type, is_high_score = False):
        if state_type == "MENU":
            from app.states.menu_state import MenuState
            view = MenuState(self)
            self.window.show_view(view)
            
        elif state_type == "PLAY":
            from app.states.play_state import PlayState
            view = PlayState(self)
            self.window.show_view(view)
            
        elif state_type == "PAUSE":
            from app.states.pause_state import PauseState
            current_game_view = self.window.current_view
            view = PauseState(self, current_game_view)
            self.window.show_view(view)

        elif state_type == "LOSE":
            from app.states.lose_state import LoseState
            view = LoseState(self)
            self.window.show_view(view)
            
        elif state_type == "WIN":
            from app.states.win_state import WinState
            view = WinState(self, is_high_score)
            self.window.show_view(view)

    def reset_game(self):
        self.score = 0
        self.game_time = 0
        self.current_level = 1
        self.is_paused = False
        
        self.player = None
        self.enemies.clear()
        #TODO maybe remove these from reset? not sure
        self.spawner = None
        self.physics_handler = None

    def quit_game(self):
        arcade.close_window()