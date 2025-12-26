import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BACKGROUND_MENU, COLOR_TEXT

class MenuState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.background_color = COLOR_BACKGROUND_MENU

    def on_show_view(self):
        arcade.set_background_color(self.background_color)

    def on_draw(self):
        self.clear()
        
        # Draw Title
        arcade.draw_text(
            "HORIZON",
            self.window.width / 2,
            self.window.height / 2 + 100,
            COLOR_TEXT,
            font_size=70,
            anchor_x="center",
            bold=True
        )
        arcade.draw_text(
            "Can you survive?",
            self.window.width / 2,
            self.window.height / 2 + 40,
            (200, 200, 255),
            font_size=20,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press ENTER to Start",
            self.window.width / 2,
            self.window.height / 2 - 20,
            COLOR_TEXT,
            font_size=10,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press ESC to Quit",
            self.window.width / 2,
            self.window.height / 2 - 50,
            COLOR_TEXT,
            font_size=10,
            anchor_x="center"
        )

        arcade.draw_text(
            f"High Score: {self.brain.high_score}",
            self.window.width / 2,
            self.window.height / 2 - 120,
            (255, 215, 0),
            font_size=16,
            anchor_x="center"
        )
        arcade.draw_text(
            "WASD to move | SPACE to attack",
            self.window.width / 2,
            50,
            (180, 180, 180),
            font_size=14,
            anchor_x="center"
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            print("User requested START game")
            self.brain.set_state("CHARACTER_SELECT")
            
        elif symbol == arcade.key.ESCAPE:
            self.brain.quit_game()