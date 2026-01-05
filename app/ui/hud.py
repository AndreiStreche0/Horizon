import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class HUD:
    def __init__(self):
        self.camera = arcade.camera.Camera2D()
        self.messages = []

    def add_message(self, text, color=arcade.color.WHITE, duration=1.0):
        self.messages.append({
            'text': text,
            'color': color,
            'time': duration,
        })
    def remove_message(self, message):
        self.messages.remove(message)
    
    def update(self, delta_time):
        for msg in self.messages:
            msg['time'] -= delta_time
            if (msg['time'] < 0):
                self.remove_message(msg)

        self.bar_width = 200
        self.bar_height = 20
        self.bg_x = (SCREEN_WIDTH // 2) - (self.bar_width / 2)
        self.bg_y = SCREEN_HEIGHT - 20 - (self.bar_height / 2)

        self.hp_text = arcade.Text(
            text="",
            x=SCREEN_WIDTH // 2 - 90,
            y=SCREEN_HEIGHT - 40,
            color=arcade.color.WHITE,
            font_size=14,
            anchor_x="center",
        )
        self.score_text = arcade.Text(
            text="",
            x=20,
            y=SCREEN_HEIGHT - 30,
            color=arcade.color.WHITE,
            font_size=18,
        )
        self.level_text = arcade.Text(
            text="",
            x=20,
            y=SCREEN_HEIGHT - 60,
            color=arcade.color.GOLD,
            font_size=16,
        )
        self.xp_text = arcade.Text(
            text="",
            x=SCREEN_WIDTH - 300,
            y=SCREEN_HEIGHT - 30,
            color=arcade.color.CYAN,
            font_size=16,
            anchor_x="center",
        )
        self.pause_text = arcade.Text(
            text="ESC: Pause",
            x=SCREEN_WIDTH - 100,
            y=20,
            color=(180, 180, 180),
            font_size=12,
        )
        self.wave_text = arcade.Text(
            text="",
            x=SCREEN_WIDTH - 120,
            y=SCREEN_HEIGHT - 30,
            color=arcade.color.ORANGE,
            font_size=16,
            anchor_x="center",
        )
        self.enemy_text = arcade.Text(
            text="",
            x=SCREEN_WIDTH - 120,
            y=SCREEN_HEIGHT - 55,
            color=arcade.color.LIGHT_GRAY,
            font_size=14,
            anchor_x="center",
        )
        self.time_text = arcade.Text(
            text="",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT - 100,
            color=arcade.color.LIGHT_GRAY,
            font_size=16,
            anchor_x="center",
        )

    def draw(self, player, score, wave_info, game_time):
        self.camera.use()

        #health bar
        bg_rect = arcade.rect.XYWH(self.bg_x, self.bg_y, self.bar_width, self.bar_height)
        arcade.draw_rect_filled(bg_rect, (50, 50, 50))

        health_percentage = player.current_hp / player.max_hp
        health_width = 196 * health_percentage
        if player.current_hp > 50:
            health_color = (0, 255, 0)
        elif player.current_hp > 25:
            health_color = (255, 165, 0)
        else:
            health_color = (255, 0, 0)

        fill_rect = arcade.rect.XYWH(self.bg_x, self.bg_y, health_width, self.bar_height)
        arcade.draw_rect_filled(fill_rect, health_color)

        #text
        hp_val = round(player.current_hp)
        self.hp_text.text = f"HP: {hp_val}/{player.max_hp}"
        self.hp_text.draw()

        score_val = round(score)
        self.score_text.text = f"Score: {score_val}"
        self.score_text.draw()

        self.level_text.text = f"Level: {player.level}"
        self.level_text.draw()

        needed_xp = player.level * 100
        xp_val = round(player.xp)
        self.xp_text.text = f"XP: {xp_val}/{needed_xp}"
        self.xp_text.draw()

        y_offset = 0
        for msg in self.messages:
            arcade.draw_text(
                msg['text'],
                window.width - 200,
                window.height / 2 + 300 + y_offset,
                msg['color'],
                font_size=30,
                anchor_x="center",
                bold=True
            )
            y_offset += 40

        self.pause_text.draw()

        if wave_info:
            self.wave_text.text = f"Wave: {wave_info['wave']}"
            self.wave_text.draw()

            self.enemy_text.text = f"Enemies: {wave_info['enemies_remaining']}/{wave_info['total_enemies']}"
            self.enemy_text.draw()

            minutes = int(game_time // 60)
            seconds = int(game_time % 60)
            self.time_text.text = f"{minutes:02d}:{seconds:02d}"
            self.time_text.draw()
