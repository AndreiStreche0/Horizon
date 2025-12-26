import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class HUD:
    def __init__(self):
        self.camera = arcade.camera.Camera2D()

    def draw(self, player, score, wave_info, game_time):
        self.camera.use()
        #health bar
        bar_width = 200
        bar_height = 20
        bg_x = (SCREEN_WIDTH // 2) - (bar_width / 2)
        bg_y = SCREEN_HEIGHT - 20 - (bar_height / 2)
        bg_rect = arcade.rect.XYWH(bg_x, bg_y, bar_width, bar_height)
        arcade.draw_rect_filled(bg_rect, (50, 50, 50))

        health_percentage = player.current_hp / player.max_hp
        health_width = 196 * health_percentage
        if player.current_hp > 50:
            health_color = (0, 255, 0)
        elif player.current_hp > 25:
            health_color = (255, 165, 0)
        else:
            health_color = (255, 0, 0)
        
        fill_rect = arcade.rect.XYWH(bg_x, bg_y, health_width, bar_height)
        arcade.draw_rect_filled(fill_rect, health_color)

        player.current_hp = round(player.current_hp)
        #hp display
        arcade.draw_text(
            text=f"HP: {player.current_hp}/{player.max_hp}",
            x=SCREEN_WIDTH // 2 - 90,
            y=SCREEN_HEIGHT - 40,
            color=arcade.color.WHITE,
            font_size=14,
            anchor_x="center"
        )
        #score display
        score = round(score)
        arcade.draw_text(
            text=f"Score: {score}",
            x=20,
            y=SCREEN_HEIGHT - 30,
            color=arcade.color.WHITE,
            font_size=18
        )
        
        # level display
        arcade.draw_text(
            text=f"Level: {player.level}",
            x=20,
            y=SCREEN_HEIGHT - 60,
            color=arcade.color.GOLD,
            font_size=16
        )
        
        #XP display
        needed_xp = player.level * 100
        player.xp = round(player.xp)
        arcade.draw_text(
            f"XP: {player.xp}/{needed_xp}",
            SCREEN_WIDTH - 300,
            SCREEN_HEIGHT - 30,
            arcade.color.CYAN,
            16,
            anchor_x="center"
        )

        #pause instruction display
        arcade.draw_text(
            "ESC: Pause",
            SCREEN_WIDTH - 100,
            20,
            (180, 180, 180),
            12
        )
        if wave_info:
            #wave info
            arcade.draw_text(
                text=f"Wave: {wave_info['wave']}",
                x=SCREEN_WIDTH - 120,
                y=SCREEN_HEIGHT - 30,
                color=arcade.color.ORANGE,
                font_size=16,
                anchor_x="center"
            )
            #enemy info
            arcade.draw_text(
                text=f"Enemies: {wave_info['enemies_remaining']}/{wave_info['total_enemies']}",
                x=SCREEN_WIDTH - 120,
                y=SCREEN_HEIGHT - 55,
                color=arcade.color.LIGHT_GRAY,
                font_size=14,
                anchor_x="center"
            )
            minutes = int(game_time // 60)
            seconds = int(game_time % 60)
            time_text = f"{minutes:02d}:{seconds:02d}"
            #time info
            arcade.draw_text(
                text=time_text,
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT - 100,
                color=arcade.color.LIGHT_GRAY,
                font_size=16,
                anchor_x="center"
        )
        # TODO: maybe progress bar thowards winning game (time passed or nr of dead enemies)
        pass