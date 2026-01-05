import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BACKGROUND_MENU, COLOR_TEXT
from storage.io import LeaderboardManager

class LeaderboardState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.background_color = COLOR_BACKGROUND_MENU
        self.leaderboard_manager = LeaderboardManager()
        self.scores = self.leaderboard_manager.get_top_scores(10)

    def on_show_view(self):
        arcade.set_background_color(self.background_color)

    def on_draw(self):
        self.clear()
        
        cx = self.window.width / 2
        cy = self.window.height / 2

        # Title
        arcade.draw_text(
            "LEADERBOARD",
            cx, self.window.height - 80,
            COLOR_TEXT,
            font_size=60,
            anchor_x="center",
            bold=True
        )

        # Column headers
        header_y = self.window.height - 150
        arcade.draw_text(
            "RANK",
            50, header_y,
            (150, 200, 255),
            font_size=16,
            anchor_x="left",
            bold=True
        )
        arcade.draw_text(
            "PLAYER",
            200, header_y,
            (150, 200, 255),
            font_size=16,
            anchor_x="left",
            bold=True
        )
        arcade.draw_text(
            "SCORE",
            cx + 100, header_y,
            (150, 200, 255),
            font_size=16,
            anchor_x="left",
            bold=True
        )

        # Draw separator line
        arcade.draw_line(50, header_y - 10, self.window.width - 50, header_y - 10, (100, 100, 100), 2)

        # Scores list
        if self.scores:
            y_offset = header_y - 50
            for rank, (username, score) in enumerate(self.scores, 1):
                color = COLOR_TEXT
                if rank == 1:
                    color = (255, 215, 0)  # Gold
                elif rank == 2:
                    color = (192, 192, 192)  # Silver
                elif rank == 3:
                    color = (205, 127, 50)  # Bronze

                arcade.draw_text(
                    str(rank),
                    50, y_offset,
                    color,
                    font_size=14,
                    anchor_x="left"
                )
                arcade.draw_text(
                    username,
                    200, y_offset,
                    color,
                    font_size=14,
                    anchor_x="left"
                )
                arcade.draw_text(
                    str(int(score)),
                    cx + 100, y_offset,
                    color,
                    font_size=14,
                    anchor_x="left"
                )
                y_offset -= 30
        else:
            arcade.draw_text(
                "No scores yet!",
                cx, cy,
                (150, 150, 150),
                font_size=20,
                anchor_x="center"
            )

        # Instructions
        arcade.draw_text(
            "Press ESC to go back to menu",
            cx, 50,
            (150, 150, 150),
            font_size=12,
            anchor_x="center"
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.brain.set_state("MENU")