import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BACKGROUND_MENU, COLOR_TEXT, PLAYABLE_CHARACTERS
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class CharacterSelectState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.characters = list(PLAYABLE_CHARACTERS.keys())
        self.selected_index = 0
        
        # Performance fix: Use SpriteList instead of individual sprite.draw()
        self.character_sprite_list = arcade.SpriteList()
        self.character_sprites = {}
        
        self.character_textures = {}
        self.animation_timers = {}
        self.current_frame = {}
        self.animation_speed = 0.1
        
        # Performance fix: Static Text Objects
        self.title_text = arcade.Text(
            "CHOOSE YOUR CHARACTER",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT - 100,
            COLOR_TEXT,
            font_size=40,
            anchor_x="center",
            bold=True
        )
        
        self.instruction_text = arcade.Text(
            "Use LEFT/RIGHT arrows to select | Press ENTER to confirm | ESC to go back",
            SCREEN_WIDTH / 2,
            50,
            COLOR_TEXT,
            font_size=12,
            anchor_x="center"
        )
        
        self.load_character_animations()
        
    def load_character_animations(self):
        for char_key in self.characters:
            char_data = PLAYABLE_CHARACTERS[char_key]
            frame_count = char_data["animations_frames"]["idle"]
            
            sprite = arcade.Sprite()
            sprite.scale = 1.5
            self.character_sprites[char_key] = sprite
            # Add to the SpriteList for rendering
            self.character_sprite_list.append(sprite)
            
            textures = []
            folder = BASE_DIR / f"assets/player/{char_data['folder']}/idle"
            
            for i in range(frame_count):
                texture_path = folder / f"idle_{i}.png"
                try:
                    texture = arcade.load_texture(str(texture_path))
                    textures.append(texture)
                except Exception as e:
                    print(f"Warning: Could not load texture {texture_path}: {e}")
            
            self.character_textures[char_key] = textures
            self.animation_timers[char_key] = 0
            self.current_frame[char_key] = 0
            
            # Set initial texture
            if textures:
                sprite.texture = textures[0]
        
    def on_show_view(self):
        arcade.set_background_color(COLOR_BACKGROUND_MENU)
    
    def on_update(self, delta_time):
        for char_key in self.characters:
            if char_key in self.character_textures and self.character_textures[char_key]:
                self.animation_timers[char_key] += delta_time
                
                if self.animation_timers[char_key] >= self.animation_speed:
                    self.animation_timers[char_key] = 0
                    textures = self.character_textures[char_key]
                    self.current_frame[char_key] = (self.current_frame[char_key] + 1) % len(textures)
                    self.character_sprites[char_key].texture = textures[self.current_frame[char_key]]
    
    def on_draw(self):
        self.clear()
        
        self.title_text.draw()
        
        start_x = SCREEN_WIDTH / 4
        spacing = SCREEN_WIDTH / 4
        
        for i, char_key in enumerate(self.characters):
            char_data = PLAYABLE_CHARACTERS[char_key]
            x_pos = start_x + (i * spacing)
            y_pos = SCREEN_HEIGHT / 2
            
            # Update sprite position before drawing list
            sprite = self.character_sprites[char_key]
            sprite.center_x = x_pos
            sprite.center_y = y_pos + 40

            if i == self.selected_index:
                arcade.draw_lbwh_rectangle_outline(
                    x_pos - 100, y_pos - 200, 200, 420,
                    arcade.color.GOLD, border_width=4
                )
            
            # Dynamic text (Stats) - For pure optimization, 
            # these could also be pre-created in __init__
            arcade.draw_text(
                char_data["name"], x_pos, y_pos - 80,
                (255, 215, 0) if i == self.selected_index else COLOR_TEXT,
                font_size=24, anchor_x="center", bold=(i == self.selected_index)
            )
            
            stats_y = y_pos - 130
            arcade.draw_text(f"HP: {char_data['hp']}", x_pos, stats_y, COLOR_TEXT, font_size=12, anchor_x="center")
            arcade.draw_text(f"Speed: {char_data['speed']}", x_pos, stats_y - 20, COLOR_TEXT, font_size=12, anchor_x="center")
            arcade.draw_text(f"Damage: {char_data['damage']}", x_pos, stats_y - 40, COLOR_TEXT, font_size=12, anchor_x="center")
            arcade.draw_text(char_data["description"], x_pos, stats_y - 65, arcade.color.GRAY, font_size=10, anchor_x="center", width=180)

        # Draw all character sprites at once
        self.character_sprite_list.draw()
        self.instruction_text.draw()
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.LEFT:
            self.selected_index = (self.selected_index - 1) % len(self.characters)
        elif symbol == arcade.key.RIGHT:
            self.selected_index = (self.selected_index + 1) % len(self.characters)
        elif symbol == arcade.key.ENTER:
            self.brain.selected_character = self.characters[self.selected_index]
            self.brain.set_state("PLAY")
        elif symbol == arcade.key.ESCAPE:
            self.brain.set_state("MENU")