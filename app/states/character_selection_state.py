import arcade
import threading
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_BACKGROUND_MENU, COLOR_TEXT, PLAYABLE_CHARACTERS, ENEMIES
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class CharacterSelectState(arcade.View):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.characters = list(PLAYABLE_CHARACTERS.keys())
        self.selected_index = 0

        self.character_sprite_list = arcade.SpriteList()
        self.character_sprites = {}

        self.character_textures = {}
        self.animation_timers = {}
        self.current_frame = {}
        self.animation_speed = 0.08

        # Loading state
        self.is_loading = False
        self.loading_progress = 0.0
        self.loading_complete = False
        self.loading_thread = None

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

        self.loading_text = arcade.Text(
            "Loading...",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 60,
            COLOR_TEXT,
            font_size=24,
            anchor_x="center"
        )

        self.load_character_animations()
        self.build_character_texts()

    def load_character_animations(self):
        for char_key in self.characters:
            char_data = PLAYABLE_CHARACTERS[char_key]
            frame_count = char_data["animations_frames"]["idle"]

            sprite = arcade.Sprite()
            sprite.scale = 1.5
            self.character_sprites[char_key] = sprite
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

            if textures:
                sprite.texture = textures[0]

    def build_character_texts(self):
        self.character_text_objects = {}
        for char_key in self.characters:
            data = PLAYABLE_CHARACTERS[char_key]

            name_normal = arcade.Text(
                data["name"],
                0,
                0,
                COLOR_TEXT,
                font_size=24,
                anchor_x="center",
                bold=False
            )
            name_selected = arcade.Text(
                data["name"],
                0,
                0,
                (255, 215, 0),
                font_size=24,
                anchor_x="center",
                bold=True
            )

            stats_hp = arcade.Text(f"HP: {data['hp']}", 0, 0, COLOR_TEXT, font_size=12, anchor_x="center")
            stats_speed = arcade.Text(f"Speed: {data['speed']}", 0, 0, COLOR_TEXT, font_size=12, anchor_x="center")
            stats_damage = arcade.Text(f"Damage: {data['damage']}", 0, 0, COLOR_TEXT, font_size=12, anchor_x="center")

            description = arcade.Text(
                data["description"],
                0,
                0,
                arcade.color.GRAY,
                font_size=10,
                anchor_x="center",
                width=180
            )

            self.character_text_objects[char_key] = {
                "name_normal": name_normal,
                "name_selected": name_selected,
                "stats": [stats_hp, stats_speed, stats_damage],
                "description": description
            }

    def preload_enemy_assets(self):
        from app.entities.enemy import get_enemy_assets
        
        enemy_types = list(ENEMIES.keys())
        total = len(enemy_types)
        
        for i, enemy_type in enumerate(enemy_types):
            try:
                get_enemy_assets(enemy_type)
                self.loading_progress = (i + 1) / total
            except Exception as e:
                print(f"Error loading {enemy_type}: {e}")
                self.loading_progress = (i + 1) / total
        
        self.loading_complete = True

    def start_loading(self):
        self.is_loading = True
        self.loading_progress = 0.0
        self.loading_complete = False
        self.loading_thread = threading.Thread(target=self.preload_enemy_assets, daemon=True)
        self.loading_thread.start()

    def on_show_view(self):
        arcade.set_background_color(COLOR_BACKGROUND_MENU)

    def on_update(self, delta_time):
        # Check if loading is complete and transition to play state
        if self.loading_complete:
            self.brain.set_state("PLAY")
            return

        # Animate character sprites
        if not self.is_loading:
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

        if self.is_loading:
            # Draw loading screen
            self.loading_text.draw()

            # Progress bar
            bar_width = 400
            bar_height = 30
            bar_x = SCREEN_WIDTH / 2 - bar_width / 2
            bar_y = SCREEN_HEIGHT / 2

            # Background
            arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, bar_width, bar_height, (50, 50, 50))

            # Progress fill
            progress_width = bar_width * self.loading_progress
            arcade.draw_lbwh_rectangle_filled(bar_x, bar_y, progress_width, bar_height, (0, 255, 0))

            # Border
            arcade.draw_lbwh_rectangle_outline(bar_x, bar_y, bar_width, bar_height, arcade.color.WHITE, border_width=2)

            # Percentage text
            percentage_text = arcade.Text(
                f"{int(self.loading_progress * 100)}%",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2 - 40,
                COLOR_TEXT,
                font_size=18,
                anchor_x="center"
            )
            percentage_text.draw()
        else:
            # Draw character selection screen
            self.title_text.draw()

            start_x = SCREEN_WIDTH / 4
            spacing = SCREEN_WIDTH / 4

            for i, char_key in enumerate(self.characters):
                char_data = PLAYABLE_CHARACTERS[char_key]
                x_pos = start_x + (i * spacing)
                y_pos = SCREEN_HEIGHT / 2

                sprite = self.character_sprites[char_key]
                sprite.center_x = x_pos
                sprite.center_y = y_pos + 40

                if i == self.selected_index:
                    arcade.draw_lbwh_rectangle_outline(
                        x_pos - 100, y_pos - 200, 200, 420,
                        arcade.color.GOLD, border_width=4
                    )

                name_texts = self.character_text_objects[char_key]
                if i == self.selected_index:
                    name = name_texts["name_selected"]
                else:
                    name = name_texts["name_normal"]

                name.x = x_pos
                name.y = y_pos - 80
                name.draw()

                stats_y = y_pos - 130
                stats_hp, stats_speed, stats_damage = name_texts["stats"]

                stats_hp.x = x_pos
                stats_hp.y = stats_y
                stats_hp.draw()

                stats_speed.x = x_pos
                stats_speed.y = stats_y - 20
                stats_speed.draw()

                stats_damage.x = x_pos
                stats_damage.y = stats_y - 40
                stats_damage.draw()

                desc = name_texts["description"]
                desc.x = x_pos
                desc.y = stats_y - 65
                desc.draw()

            self.character_sprite_list.draw()
            self.instruction_text.draw()

    def on_key_press(self, symbol, modifiers):
        if self.is_loading:
            return  # Ignore input during loading

        if symbol == arcade.key.LEFT:
            self.selected_index = (self.selected_index - 1) % len(self.characters)
        elif symbol == arcade.key.RIGHT:
            self.selected_index = (self.selected_index + 1) % len(self.characters)
        elif symbol == arcade.key.ENTER:
            self.brain.selected_character = self.characters[self.selected_index]
            self.start_loading()
        elif symbol == arcade.key.ESCAPE:
            self.brain.set_state("MENU")