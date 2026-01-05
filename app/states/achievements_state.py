import arcade
import arcade.gui
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_TEXT, COLOR_BACKGROUND_MENU
from app.achievements.achievement import AchievementTier
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BACKGROUND_MENU, COLOR_TEXT

class AchievementsState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.background_color = COLOR_BACKGROUND_MENU
        self.scroll_y = 0
        self.icon_size = 80
        self.selected_index = 0
        self.achievement_height = 100
        
        self.title_text = arcade.Text(
            "ACHIEVEMENTS",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 60,
            COLOR_TEXT,
            font_size=50,
            anchor_x="center",
            bold=True
        )
        
        self.controls_text = arcade.Text(
            "UP/DOWN: Navigate | ESC: Back",
            SCREEN_WIDTH / 2,
            30,
            (150, 150, 150),
            font_size=11,
            anchor_x="center"
        )

        # Get user achievements
        self.achievements = self.brain.achievement_manager.get_user_achievements(
            self.brain.username
        )
        
    def on_show_view(self):
        arcade.set_background_color(self.background_color)
    
    def on_draw(self):
        self.clear()
        
        #draw title
        self.title_text.draw()
        
        #calculate visible area
        visible_start = max(0, int(self.scroll_y / self.achievement_height))
        visible_end = min(len(self.achievements), visible_start + 5)
        
        y_pos = SCREEN_HEIGHT - 140
        for i in range(visible_start, visible_end):
            achievement = self.achievements[i]
            
            #highlight selected
            if i == self.selected_index:
                rect = arcade.rect.XYWH(SCREEN_WIDTH / 2, y_pos - 40, SCREEN_WIDTH - 40, self.achievement_height)
                arcade.draw_rect_filled(rect, (50, 50, 80))
            
            #draw icon
            try:
                icon_path = f"assets/achievement_icons/{achievement.name}.png"
                icon = arcade.load_texture(icon_path)
                arcade.draw_texture_rect(
                    icon, 
                    arcade.rect.XYWH(30 + self.icon_size/2, y_pos - self.icon_size/2, self.icon_size, self.icon_size)
                )
            except Exception:
                #placeholder
                rect_outline = arcade.rect.XYWH(30 + self.icon_size // 2, y_pos - self.icon_size // 2, self.icon_size, self.icon_size)
                arcade.draw_rect_outline(rect_outline, (150, 150, 150), border_width=2)
            
            title_text_str = achievement.name
            if achievement.is_unlocked():
                tier_name = achievement.get_tier_name(achievement.unlockedTier)
                title_text_str += f" [{tier_name}]"
                color = (255, 215, 0) if achievement.unlockedTier.name == "GOLD" else \
                        (192, 192, 192) if achievement.unlockedTier.name == "SILVER" else \
                        (205, 127, 50)
            else:
                color = (100, 100, 100)

            arcade.draw_text(title_text_str, 130, y_pos - 10, color, 14, bold=True)
            
            description = self._format_description(achievement)
            
            arcade.draw_text(
                description, 130, y_pos - 40, 
                (180, 180, 180) if achievement.is_unlocked() else (100, 100, 100),
                font_size=11, width=int(SCREEN_WIDTH - 170), multiline=True
            )
            
            y_pos -= self.achievement_height
        
        self.controls_text.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.brain.set_state("MENU")
        
        elif symbol == arcade.key.UP:
            self.selected_index = max(0, self.selected_index - 1)
            self.scroll_y = max(0, self.scroll_y - self.achievement_height)
        
        elif symbol == arcade.key.DOWN:
            self.selected_index = min(len(self.achievements) - 1, self.selected_index + 1)
            self.scroll_y = min(
                (len(self.achievements) - 5) * self.achievement_height,
                self.scroll_y + self.achievement_height
            )
    
    def _format_description(self, achievement):
        if not achievement.is_unlocked():
            return f"Bronze Requirement - {achievement.get_description_for_tier(AchievementTier.BRONZE)}"
        if achievement.unlockedTier == AchievementTier.BRONZE:
            return f"Silver Requirement - {achievement.get_description_for_tier(AchievementTier.SILVER)}"
        if achievement.unlockedTier == AchievementTier.SILVER:
            return f"Gold Requirement - {achievement.get_description_for_tier(AchievementTier.GOLD)}"
        return achievement.get_description_for_tier(AchievementTier.GOLD)