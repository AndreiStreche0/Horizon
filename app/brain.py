import arcade
from storage.authentification import AuthentificationManager
from app.states.menu_state import MenuState
from app.states.play_state import PlayState
from app.states.pause_state import PauseState
from app.states.lose_state import LoseState
from app.states.win_state import WinState
from app.states.login_state import LoginState
from app.states.leaderboard_state import LeaderboardState
from app.states.character_selection_state import CharacterSelectState

#handles game state and current session
class Brain:
    def __init__(self, window):
        self.window = window
        self.authentificator = AuthentificationManager()

        self.score = 0
        self.current_level = 1
        if self.authentificator.current_user:
            self.username = self.authentificator.current_user
        else:
            self.username = "Anonymous"
        self.high_score = self.authentificator.get_current_high_score()
        self.game_time = 0
        self.is_paused = False
        #default character
        self.selected_character = "knight"
        self.player = None
        self.enemies = []
        self.current_map = None
        self.spawner = None
        self.physics_handler = None
        self.hud = None

    def set_state(self, state_type, is_high_score = False):
        if state_type == "MENU":
            view = MenuState(self)
            self.window.show_view(view)
            
        elif state_type == "CHARACTER_SELECT":
            view = CharacterSelectState(self)
            self.window.show_view(view)
            
        elif state_type == "PLAY":
            view = PlayState(self)
            self.window.show_view(view)
            
        elif state_type == "PAUSE":
            current_game_view = self.window.current_view
            view = PauseState(self, current_game_view)
            self.window.show_view(view)

        elif state_type == "LOSE":
            view = LoseState(self)
            self.window.show_view(view)
            
        elif state_type == "WIN":
            view = WinState(self, is_high_score)
            self.window.show_view(view)
        elif state_type == "LOGIN":
            view = LoginState(self)
            self.window.show_view(view)
        elif state_type == "LEADERBOARD":
            view = LeaderboardState(self)
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

    #TODO change after implementing login logic from menu
    def set_user(self, new_username):
        self.authentificator.login(new_username)
        self.username = self.authentificator.current_user
        self.high_score = self.authentificator.get_current_high_score()

    def new_score(self, new_score):
        if new_score > self.high_score:
            self.high_score = round(new_score)
            self.authentificator.save_new_score(round(new_score))

    def quit_game(self):
        arcade.close_window()