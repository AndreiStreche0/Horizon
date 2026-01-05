import arcade
import arcade.gui
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_TEXT, COLOR_BACKGROUND_MENU

class LoginState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout(vertical=True, space_between=20)

        #title
        title_label = arcade.gui.UILabel(
            text="Enter Username",
            text_color=COLOR_TEXT,
            font_size=20,
            height=40
        )
        self.v_box.add(title_label)

        self.input_field = arcade.gui.UIInputText(
            text=self.brain.username,
            width=300,
            height=40,
            text_color=arcade.color.GHOST_WHITE,
            font_size=18,
        )

        self.input_wrapper = self.input_field.with_background(
            color=arcade.color.LILAC
        ).with_border(
            width=2, 
            color=arcade.color.WHITE
        )
        
        self.v_box.add(self.input_wrapper)

        anchor_layout = arcade.gui.UIAnchorLayout()
        
        anchor_layout.add(
            child=self.v_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )

        self.manager.add(anchor_layout)

    def on_draw(self):
        self.clear()
        
        bg_rect = arcade.rect.XYWH(0, 0, self.window.width, self.window.height)
        arcade.draw_rect_filled(bg_rect, COLOR_BACKGROUND_MENU)
        
        #input box
        self.manager.draw()
        
        #instructions for login
        arcade.draw_text(
            "Press ENTER to confirm",
            x=SCREEN_WIDTH / 2,
            y=SCREEN_HEIGHT / 2 - 150,
            color=(150, 150, 150),
            font_size=12,
            anchor_x="center"
        )

    def on_key_press(self, symbol, modifiers):
        #enter for submit
        if symbol == arcade.key.ENTER:
            new_name = self.input_field.text
            if len(new_name) > 0:
                self.brain.set_user(new_name)
                self.brain.set_state("MENU")
        #escape for leaving
        elif symbol == arcade.key.ESCAPE:
            self.brain.set_state("MENU")

    def on_hide_view(self):
        self.manager.disable()