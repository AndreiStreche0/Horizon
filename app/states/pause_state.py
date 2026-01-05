import arcade
from arcade import LBWH

from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BACKGROUND_MENU, COLOR_TEXT
class PauseState(arcade.View):
    def __init__(self, brain, previous_view):
        super().__init__()
        self.brain = brain
        self.brain.is_paused = True
        self.previous_view = previous_view

    def on_show_view(self):
        pass
    def on_draw(self):
        self.clear()

        if self.previous_view:
            self.previous_view.on_draw()

        self.window.default_camera.use()

        overlay_rect = LBWH(0, 0, self.window.width, self.window.height)
        arcade.draw_rect_filled(overlay_rect, (0, 0, 0, 150))
        
        #draw pause text
        arcade.draw_text(
            "PAUSED",
            self.window.width / 2,
            self.window.height / 2 + 50,
            COLOR_TEXT,
            font_size=50,
            anchor_x="center",
            bold=True
        )
        
        #drraw options
        arcade.draw_text(
            "[ESC] - Resume Game",
            self.window.width / 2,
            self.window.height / 2 - 20,
            COLOR_TEXT,
            font_size=20,
            anchor_x="center"
        )
        
        #draw exit
        arcade.draw_text(
            "[Q] - Quit to Menu",
            self.window.width / 2,
            self.window.height / 2 - 60,
            COLOR_TEXT,
            font_size=20,
            anchor_x="center"
        )
        
        self.brain.score = round(self.brain.score)
        #draw current score
        arcade.draw_text(
            f"Score: {self.brain.score}",
            self.window.width / 2,
            self.window.height / 2 - 120,
            (255, 215, 0),  # Gold
            font_size=24,
            anchor_x="center"
        )
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            #resume game
            self.brain.is_paused = False
            self.window.show_view(self.previous_view)
            
        elif symbol == arcade.key.Q:
            #quit to main menu
            self.brain.reset_game()
            self.brain.set_state("MENU")