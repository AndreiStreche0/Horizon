import arcade
import arcade.gui
from app.achievements.achievement import ACHIEVEMENT_LIST
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_TEXT, COLOR_BACKGROUND_MENU

class AchievementState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.medal_gold_tex = arcade.load_texture(":resources:images/items/coinGold.png")
        self.medal_silver_tex = arcade.load_texture(":resources:images/items/coinSilver.png")
        self.medal_bronze_tex = arcade.load_texture(":resources:images/items/coinBronze.png")
        self.medal_none_tex = arcade.load_texture(":resources:onscreen_controls/shaded_dark/x.png")

        #main vertical box layout
        self.v_box = arcade.gui.UIBoxLayout(vertical=True, space_between=8)

        #title
        title = arcade.gui.UILabel(
            text="ACHIEVEMENTS",
            text_color=arcade.color.GOLD,
            font_size=22,
            height=40,
            bold=True
        )
        self.v_box.add(title)

        for ach in ACHIEVEMENT_LIST:
            current_val = self.brain.achievements.achievement_progress(ach.name)
            if current_val == 9999999: current_val = 0
            
            bronze_value, silver_value, gold_value = ach.tiers
            medal_type, next_goal_text = self.brain.achievements.get_medal_info(ach.name)
            medal_texture = self.medal_none_tex
            target_val = bronze_value
            if medal_type == "GOLD": 
                medal_texture = self.medal_gold_tex
                target_val = gold_value
            elif medal_type == "SILVER": 
                medal_texture = self.medal_silver_tex
                target_val = gold_value
            elif medal_type == "BRONZE": 
                medal_texture = self.medal_bronze_tex
                target_val = silver_value

            row = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
            
            #left : name and the next rank
            current_val = round(current_val)
            val_str = str(current_val)
            target_str = str(target_val)
            desc_text = f"{ach.description} - {val_str} / {target_str}"
            
            row = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
            text_column = arcade.gui.UIBoxLayout(vertical=True, space_between=4, align="left")

            name_label = arcade.gui.UILabel(
                text=ach.name,
                text_color=arcade.color.DARK_VIOLET,
                font_size=16,
                width=450,
                align="left",
                bold=True
            )
            desc_label = arcade.gui.UILabel(
                text=desc_text,
                text_color=arcade.color.PLUM,
                font_size=12,
                width=450,
                align="left"
            )
            text_column.add(name_label)
            text_column.add(desc_label)
            
            row.add(text_column)
            
            if medal_texture:
                icon = arcade.gui.UITextureButton(
                    texture=medal_texture,
                    width=30,
                    height=30
                )
                row.add(icon)
            row_wrapper = row.with_padding(top=5, bottom=5)            
            self.v_box.add(row_wrapper)

        self.v_box.add(arcade.gui.UILabel(text=" ", height=10))
        self.v_box.add(arcade.gui.UILabel(text="Press ESC to return", text_color=arcade.color.GRAY, font_size=12))

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(self.v_box, anchor_x="center_x", anchor_y="center_y")
        self.manager.add(anchor)

    def on_draw(self):
        self.clear()
        bg_rect = arcade.rect.XYWH(0, 0, self.window.width, self.window.height)
        arcade.draw_rect_filled(bg_rect, COLOR_BACKGROUND_MENU)
        self.manager.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.brain.set_state("MENU")

    def on_hide_view(self):
        self.manager.disable()