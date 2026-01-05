import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_TEXT

class LoseState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.camera = arcade.camera.Camera2D()
        self.camera.bottom_left = (0, 0)
        
        self.window.background_color = (20, 0, 0)
        
        self.is_new_high_score = self.brain.save_score(is_win=False, player=self.brain.player)

    def on_draw(self):
        self.clear()
        self.camera.use()

        cx = self.window.width / 2
        cy = self.window.height / 2

        #title
        arcade.draw_text(
            "YOU DIED",
            x=cx, y=cy + 100,
            color=arcade.color.RED,
            font_size=60,
            anchor_x="center",
            bold=True
        )

        # Afișează "NEW HIGH SCORE!" doar dacă e cazul
        if self.is_new_high_score:
            arcade.draw_text(
                "NEW HIGH SCORE!",
                x=cx, y=cy + 40,
                color=arcade.color.CYAN,
                font_size=24,
                anchor_x="center",
                bold=True
            )

        #final score
        arcade.draw_text(
            f"Final Score: {int(self.brain.score)}",
            x=cx, y=cy - 20,
            color=COLOR_TEXT,
            font_size=30,
            anchor_x="center"
        )
        
        #next step instruction to replay
        arcade.draw_text(
            "Press [R] to Play Again",
            x=cx, y=cy - 100,
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