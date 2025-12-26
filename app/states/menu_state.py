import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BACKGROUND_MENU, COLOR_TEXT

class MenuState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain

    def on_show_view(self):
        arcade.set_background_color(COLOR_BACKGROUND_MENU)

    def on_draw(self):
        self.clear()
        
        # Draw Title
        arcade.draw_text(
            "HORIZON",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 50,
            COLOR_TEXT,
            font_size=50,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press ENTER to Start",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 20,
            COLOR_TEXT,
            font_size=14,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press ESC to Quit",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 - 50,
            COLOR_TEXT,
            font_size=10,
            anchor_x="center"
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            print("User requested START game")
            self.brain.set_state("CHARACTER_SELECT")
            
        elif symbol == arcade.key.ESCAPE:
            self.brain.quit_game()