import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_TEXT

class LoseState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.camera = arcade.camera.Camera2D()
        self.camera.bottom_left = (0, 0)
        
        self.window.background_color = (20, 0, 0)

    def on_draw(self):
        self.clear()
        self.camera.use()

        cx = self.window.width / 2
        cy = self.window.height / 2

        #title
        arcade.draw_text(
            "YOU DIED",
            x=cx, y=cy + 80,
            color=arcade.color.RED,
            font_size=60,
            anchor_x="center",
            bold=True
        )

        #final score
        arcade.draw_text(
            f"Final Score: {int(self.brain.score)}",
            x=cx, y=cy,
            color=COLOR_TEXT,
            font_size=30,
            anchor_x="center"
        )
        
        #next step instruction to replay
        arcade.draw_text(
            "Press [R] to Play Again",
            x=cx, y=cy - 80,
            color=arcade.color.YELLOW,
            font_size=20,
            anchor_x="center"
        )
        #to exit
        arcade.draw_text(
            "Press [Q] for Menu",
            x=cx, y=cy - 140,
            color=arcade.color.GOLDEN_YELLOW,
            font_size=16,
            anchor_x="center"
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.R:
            self.brain.reset_game()
            self.brain.set_state("PLAY")
        elif symbol == arcade.key.Q:
            self.brain.reset_game()
            self.brain.set_state("MENU")