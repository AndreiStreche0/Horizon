import arcade

class HUD:
    def __init__(self):
        self.camera = arcade.Camera2D()

    def draw(self, player, score):
        self.camera.use()
        # TODO: put health bar (arcade.draw_rectangle_filled)
        # TODO: score and level (arcade.draw_text)
        # TODO: maybe progress bar thowards winning game (time passed or nr of dead enemies)
        pass