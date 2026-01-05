import arcade
from config import COLOR_BACKGROUND_MENU, COLOR_TEXT
from storage.authentication import AuthenticationManager

class LoginState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.background_color = COLOR_BACKGROUND_MENU

        self.username_input = ""
        self.password_input = ""
        self.active_field = "username"
        self.cursor_visible = True
        self.cursor_timer = 0.0

        self.max_username_length = 20
        self.max_password_length = 32
        self.min_password_length = 4
        self.allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-!?")

        self.auth = AuthenticationManager()
        self.skip_initial_text = False

        cx, cy = self.window.width / 2, self.window.height / 2
        self.title_text = arcade.Text("LOGIN", cx, cy + 120, COLOR_TEXT, font_size=60,
                                      anchor_x="center", bold=True)
        self.instructions_text = arcade.Text(
            "TAB: change field | ENTER: confirm | ESC: back\n"
            f"User: max {self.max_username_length} | Password: {self.min_password_length}-{self.max_password_length} characters (letters/numbers/._-!?)",
            cx, cy - 150, (150, 150, 150), font_size=12, anchor_x="center",
            multiline=True, width=520, align="center"
        )
        self.username_text_obj = arcade.Text("", cx - 140, cy + 20, COLOR_TEXT, font_size=20,
                                             anchor_x="left", anchor_y="center")
        self.password_text_obj = arcade.Text("", cx - 140, cy - 30, COLOR_TEXT, font_size=20,
                                             anchor_x="left", anchor_y="center")
        self.status_text = arcade.Text("", cx, cy - 210, arcade.color.RED, font_size=12,
                                       anchor_x="center")

    def on_show_view(self):
        arcade.set_background_color(self.background_color)
        self.skip_initial_text = True

    def set_status(self, message, color=arcade.color.RED):
        self.status_text.text = message
        self.status_text.color = color

    def on_draw(self):
        self.clear()
        cx, cy = self.window.width / 2, self.window.height / 2
        self.title_text.draw()
        self.instructions_text.draw()

        # Username box
        arcade.draw_rect_outline(
            arcade.LRBT(cx - 180, cx + 180, cy + 15, cy + 65),
            color=(160, 200, 255) if self.active_field == "username" else (100, 150, 200),
            border_width=2
        )
        user_display = self.username_input or ""
        user_color = COLOR_TEXT if self.username_input else (140, 140, 140)
        if self.active_field == "username" and self.cursor_visible:
            user_display += "|"
        self.username_text_obj.text = user_display
        self.username_text_obj.color = user_color
        self.username_text_obj.x = cx - 170
        self.username_text_obj.y = cy + 40
        self.username_text_obj.draw()

        # Password box
        arcade.draw_rect_outline(
            arcade.LRBT(cx - 180, cx + 180, cy - 45, cy + 5),
            color=(160, 200, 255) if self.active_field == "password" else (100, 150, 200),
            border_width=2
        )
        masked = "*" * len(self.password_input) if self.password_input else ""
        pass_color = COLOR_TEXT if self.password_input else (140, 140, 140)
        if self.active_field == "password" and self.cursor_visible:
            masked += "|"
        self.password_text_obj.text = masked
        self.password_text_obj.color = pass_color
        self.password_text_obj.x = cx - 170
        self.password_text_obj.y = cy - 20
        self.password_text_obj.draw()

        arcade.draw_text("Username:", cx - 300, cy + 40, COLOR_TEXT, font_size=14, anchor_x="left", anchor_y="center")
        arcade.draw_text("Password:", cx - 300, cy - 20, COLOR_TEXT, font_size=14, anchor_x="left", anchor_y="center")
        self.status_text.draw()

    def on_update(self, delta_time):
        self.cursor_timer += delta_time
        if self.cursor_timer >= 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def try_login(self):
        if not self.username_input:
            self.set_status("No username provided!", arcade.color.RED)
            return
        if not self.password_input:
            self.set_status("No password provided!", arcade.color.RED)
            return

        if self.auth.player_exists(self.username_input) and not self.auth.validate_user(self.username_input, self.password_input):
            self.set_status("Incorrect password. Try again!", arcade.color.RED)
            return

        if not self.auth.player_exists(self.username_input) and len(self.password_input) < self.min_password_length:
            self.set_status(f"Password must be at least {self.min_password_length} characters long!", arcade.color.RED)
            return

        success, player_data = self.auth.login_or_create(self.username_input, self.password_input)
        if success and player_data:
            self.brain.username = self.username_input
            self.brain.high_score = player_data.get("best_score", 0)
            if hasattr(self.brain, "leaderboard_manager"):
                self.brain.leaderboard_manager.players = self.auth.players
            self.auth.save_players()
            self.set_status("Successful authentication!", arcade.color.LIGHT_GREEN)
            self.brain.set_state("MENU")
        else:
            self.set_status("Could not authenticate user!", arcade.color.RED)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ENTER:
            self.try_login()
        elif symbol == arcade.key.ESCAPE:
            self.brain.set_state("MENU")
        elif symbol == arcade.key.BACKSPACE:
            if self.active_field == "username" and self.username_input:
                self.username_input = self.username_input[:-1]
            elif self.active_field == "password" and self.password_input:
                self.password_input = self.password_input[:-1]
        elif symbol == arcade.key.TAB:
            self.active_field = "password" if self.active_field == "username" else "username"

    def on_text(self, text):
        if self.skip_initial_text:
            self.skip_initial_text = False
            return
        if text not in self.allowed_chars:
            return

        if self.active_field == "username":
            if len(self.username_input) < self.max_username_length:
                self.username_input += text
        else:
            if len(self.password_input) < self.max_password_length:
                self.password_input += text