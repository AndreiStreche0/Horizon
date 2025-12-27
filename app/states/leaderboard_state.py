import arcade
import arcade.gui
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_TEXT

class LeaderboardState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        #main box
        self.v_box = arcade.gui.UIBoxLayout(vertical=True, space_between=10)

        title = arcade.gui.UILabel(
            text="TOP WARRIORS",
            text_color=arcade.color.GOLD,
            font_size=24,
            height=50,
            bold=True
        )
        self.v_box.add(title)
        #for spacing
        self.v_box.add(arcade.gui.UILabel(text=" ", height=15))

        leaderboard_list = self.brain.authentificator.get_all_user_scores()[:10]

        if not leaderboard_list:
            no_scores_label = arcade.gui.UILabel(text="No scores yet.", text_color=arcade.color.LIGHT_GRAY, font_size=16)
            self.v_box.add(no_scores_label)
        else:
            place = 1
            for user in leaderboard_list:
                if user[0] == "null":
                    continue
                
                row_player_box = arcade.gui.UIBoxLayout(vertical=False, space_between=20)

                if place == 1:
                    color = arcade.color.GOLD
                elif place == 2:
                    color = arcade.color.SILVER
                elif place == 3:
                    color = arcade.color.BRONZE
                else: color = arcade.color.WHITE

                name_label = arcade.gui.UILabel(
                        text=f"{place}. {user[0]} : ",
                        text_color=color,
                        font_size=16,
                        width=200,
                        align="left"
                    )
                score_label = arcade.gui.UILabel(
                        text=str(user[1]),
                        text_color=color,
                        font_size=16,
                        width=100,
                        align="right"
                    )
                    
                row_player_box.add(name_label)
                row_player_box.add(score_label)
                
                self.v_box.add(row_player_box)
                place += 1
        
        #for spacing
        self.v_box.add(arcade.gui.UILabel(text=" ", height=20))

        exit_label = arcade.gui.UILabel(
            text="Press ESC to return",
            text_color=(150, 150, 150),
            font_size=14
        )
        self.v_box.add(exit_label)
        anchor_layout = arcade.gui.UIAnchorLayout()
        anchor_layout.add(self.v_box, anchor_x="center_x", anchor_y="center_y")
        
        self.manager.add(anchor_layout)

    def on_draw(self):
        self.clear()
        
        bg_rect = arcade.rect.XYWH(0, 0, self.window.width, self.window.height)
        arcade.draw_rect_filled(bg_rect, (20, 20, 30))
        
        self.manager.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.brain.set_state("MENU")

    def on_hide_view(self):
        self.manager.disable()