import arcade

#handles game state and current session
class Brain:
    def __init__(self, window):
        self.window = window
        
        self.score = 0
        self.current_level = 1
        self.username = "Player"

    def set_state(self, state_type):
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
            view = PauseState(self)
            self.window.show_view(view)

    def quit_game(self):
        arcade.close_window()