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

        # Main Menu Options
        arcade.draw_text(
            "Press ENTER to Start Game",
            self.window.width / 2,
            self.window.height / 2 - 20,
            COLOR_TEXT,
            font_size=14,
            anchor_x="center"
        )

        # Additional options
        arcade.draw_text(
            "Press [L] to Login",
            self.window.width / 2,
            self.window.height / 2 - 60,
            (150, 200, 255),
            font_size=12,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press [TAB] for Leaderboard",
            self.window.width / 2,
            self.window.height / 2 - 100,
            (150, 200, 255),
            font_size=12,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press [A] for Achievements",
            self.window.width / 2,
            self.window.height / 2 - 140,
            (150, 200, 255),
            font_size=12,
            anchor_x="center"
        )

        # User info
        arcade.draw_text(
            f"Current User: {self.brain.username}",
            20,
            self.window.height - 40,
            (100, 200, 255),
            font_size=14,
            anchor_x="left"
        )

        # Get games played for current user
        user_data = self.brain.leaderboard_manager.get_user_data(self.brain.username)
        games_played = user_data.get("games_played", 0) if user_data else 0
        
        arcade.draw_text(
            f"Games Played: {games_played}",
            20,
            self.window.height - 70,
            (100, 200, 255),
            font_size=12,
            anchor_x="left"
        )

        arcade.draw_text(
            f"Your High Score: {int(self.brain.high_score)}",
            self.window.width / 2,
            self.window.height / 2 - 180,
            (255, 215, 0),
            font_size=14,
            anchor_x="center"
        )

        # Controls info
        arcade.draw_text(
            "WASD or Arrows to move | Z/X/C to attack",
            self.window.width / 2,
            50,
            (180, 180, 180),
            font_size=12,
            anchor_x="center"
        )

        arcade.draw_text(
            "Press ESC to Quit",
            self.window.width / 2,
            20,
            (180, 180, 180),
            font_size=10,
            anchor_x="center"
        )

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            print("User requested START game")
            self.brain.set_state("CHARACTER_SELECT")
        
        elif symbol == arcade.key.L:
            # Login
            self.brain.set_state("LOGIN")
        
        elif symbol == arcade.key.TAB:
            # Leaderboard
            self.brain.set_state("LEADERBOARD")
            
        elif symbol == arcade.key.A:
            # Achievements
            self.brain.set_state("ACHIEVEMENTS")

        elif symbol == arcade.key.ESCAPE:
            self.brain.quit_game()