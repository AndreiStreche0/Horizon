import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_TEXT

class WinState(arcade.View):
    def __init__(self, brain, is_high_score):
        super().__init__()
        self.brain = brain
        self.is_high_score = is_high_score
        
        self.camera = arcade.camera.Camera2D()
        self.camera.bottom_left = (0, 0)
        
        self.window.background_color = (0, 50, 0)

    def on_draw(self):
        self.clear()
        self.camera.use()

        cx = self.window.width / 2
        cy = self.window.height / 2

        #title
        victory_text = arcade.Text(
            "VICTORY!",
            x=cx, y=cy + 100,
            color=arcade.color.GOLD,
            font_size=60,
            anchor_x="center",
            bold=True
        )
        victory_text.draw()
        
        #set new high score
        if self.is_high_score:
            new_high_score_text = arcade.Text(
                "NEW HIGH SCORE!",
                x=cx, y=cy + 40,
                color=arcade.color.CYAN,
                font_size=30,
                anchor_x="center",
                bold=True
            )
            new_high_score_text.draw()

        #final score
        final_score_text = arcade.Text(
            f"Final Score: {int(self.brain.score)}",
            x=cx, y=cy - 20,
            color=COLOR_TEXT,
            font_size=24,
            anchor_x="center"
        )
        final_score_text.draw()
        
        #play again
        play_again_text = arcade.Text(
            "Press [R] to Play Again",
            x=cx, y=cy - 100,
            color=arcade.color.YELLOW,
            font_size=20,
            anchor_x="center"
        )
        play_again_text.draw()

        #go to menu
        menu_text = arcade.Text(
            "Press [Q] for Menu",
            x=cx, y=cy - 140,
            color=arcade.color.WHITE,
            font_size=16,
            anchor_x="center"
        )
        menu_text.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.R:
            self.brain.reset_game()
            self.brain.set_state("PLAY")
        elif symbol == arcade.key.Q:
            self.brain.reset_game()
            self.brain.set_state("MENU")