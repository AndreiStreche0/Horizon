import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from app.brain import Brain

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.brain = Brain(self)

    def setup(self):
        self.brain.set_state("MENU")

def main():
    window = GameWindow()
    window.center_window()
    window.setup()
    arcade.run()
if __name__ == "__main__":
    main()