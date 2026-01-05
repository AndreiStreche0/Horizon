import arcade
from app.states.menu_state import MenuState
from app.states.character_selection_state import CharacterSelectState
from app.states.play_state import PlayState
from app.states.pause_state import PauseState
from app.states.lose_state import LoseState
from app.states.win_state import WinState
from app.states.login_state import LoginState
from app.states.leaderboard_state import LeaderboardState
from storage.io import LeaderboardManager
from app.achievements.achievement_manager import AchievementManager
from app.states.achievements_state import AchievementsState
from app.achievements.achievement import AchievementTier

# Handles game state and current session
class Brain:
    def __init__(self, window):
        self.window = window
        
        self.score = 0
        self.current_level = 1

        self.high_score = 0
        self.username = "Guest"
        self.selected_character = "knight"  # Default character
        self.game_time = 0
        self.is_paused = False

        self.player = None
        self.enemies = []
        self.current_map = None
        self.spawner = None
        self.physics_handler = None
        self.hud = None

        self.session_enemies_killed = 0
        self.session_distance_traveled = 0.0
        
        # Initialize leaderboard manager
        self.leaderboard_manager = LeaderboardManager()

        self.achievement_manager = AchievementManager()

    def set_state(self, state_type, is_high_score = False):
        if state_type == "MENU":
            view = MenuState(self)
            self.window.show_view(view)
            
        elif state_type == "CHARACTER_SELECT":
            view = CharacterSelectState(self)
            self.window.show_view(view)
            
        elif state_type == "PLAY":
            view = PlayState(self)
            self.window.show_view(view)
            
        elif state_type == "PAUSE":
            current_game_view = self.window.current_view
            view = PauseState(self, current_game_view)
            self.window.show_view(view)

        elif state_type == "LOSE":
            view = LoseState(self)
            self.window.show_view(view)
            
        elif state_type == "WIN":
            view = WinState(self, is_high_score)
            self.window.show_view(view)
            
        elif state_type == "LOGIN":
            view = LoginState(self)
            self.window.show_view(view)
            
        elif state_type == "LEADERBOARD":
            view = LeaderboardState(self)
            self.window.show_view(view)

        elif state_type == "ACHIEVEMENTS":
            view = AchievementsState(self)
            self.window.show_view(view)

    def reset_game(self):
        self.score = 0
        self.game_time = 0
        self.session_enemies_killed = 0
        self.session_distance_traveled = 0.0
        self.current_level = 1
        self.is_paused = False
        
        self.player = None
        self.enemies.clear()
        self.spawner = None
        self.physics_handler = None

    def save_score(self, is_win=False, player=None):
        session_time = self.game_time
        current_player = player if player else self.player
        session_damage = current_player.session_damage_taken if current_player else 0
        session_enemies = self.session_enemies_killed
        session_distance = current_player.session_distance_traveled if current_player else 0
        is_dead = not is_win

        is_new_high = self.leaderboard_manager.add_score(
            self.username, int(self.score), session_time, session_damage, session_enemies, session_distance, is_dead
        )
        # Update win streak
        best_win_streak = self.leaderboard_manager.update_win_streak(self.username, is_win)

        total_seconds = self.leaderboard_manager.get_total_time_played(self.username)
        total_damage = self.leaderboard_manager.get_total_damage_taken(self.username)
        total_enemies = self.leaderboard_manager.get_total_enemies_defeated(self.username)
        total_distance = self.leaderboard_manager.get_total_distance_traveled(self.username)
        total_deaths = self.leaderboard_manager.get_total_deaths(self.username)

        self._check_game_veteran(total_seconds)
        self._check_master_of_the_game(int(self.score))
        self._check_human_tank(total_damage)
        self._check_one_monsters_fear(total_enemies)
        self._check_traveler(total_distance)
        self._check_unstoppable(best_win_streak)
        self._check_why_do_we_fall(total_deaths)

        if is_new_high:
            self.high_score = int(self.score)
        return is_new_high
    
    def _check_game_veteran(self, total_seconds):
        minutes = total_seconds / 60.0
        thresholds = [15, 30, 60]  # Bronze, Silver, Gold
        achievement_name = "Game Veteran"
        username = self.username

        if minutes >= thresholds[2]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.GOLD)
        elif minutes >= thresholds[1]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.SILVER)
        elif minutes >= thresholds[0]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.BRONZE)

    def _check_master_of_the_game(self, score):
        thresholds = [2500, 5000, 10000]  # Bronze, Silver, Gold
        achievement_name = "Master Of The Game"
        username = self.username

        if score >= thresholds[2]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.GOLD)
        elif score >= thresholds[1]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.SILVER)
        elif score >= thresholds[0]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.BRONZE)

    def _check_human_tank(self, total_damage):
        thresholds = [1000, 1500, 2000]  # Bronze, Silver, Gold
        achievement_name = "The Human Tank"
        username = self.username

        if total_damage >= thresholds[2]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.GOLD)
        elif total_damage >= thresholds[1]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.SILVER)
        elif total_damage >= thresholds[0]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.BRONZE)

    def _check_one_monsters_fear(self, total_enemies):
        thresholds = [250, 500, 1000]  # Bronze, Silver, Gold
        achievement_name = "The One Monsters Fear"
        username = self.username

        if total_enemies >= thresholds[2]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.GOLD)
        elif total_enemies >= thresholds[1]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.SILVER)
        elif total_enemies >= thresholds[0]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.BRONZE)

    def _check_traveler(self, total_distance):
        thresholds = [20000, 50000, 80000]  # Bronze, Silver, Gold
        achievement_name = "Traveler"
        username = self.username

        if total_distance >= thresholds[2]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.GOLD)
        elif total_distance >= thresholds[1]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.SILVER)
        elif total_distance >= thresholds[0]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.BRONZE)

    def _check_unstoppable(self, win_streak):
        thresholds = [2, 4, 8]  # Bronze, Silver, Gold
        achievement_name = "Unstoppable"
        username = self.username

        if win_streak >= thresholds[2]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.GOLD)
        elif win_streak >= thresholds[1]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.SILVER)
        elif win_streak >= thresholds[0]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.BRONZE)

    def _check_why_do_we_fall(self, total_deaths):
        thresholds = [5, 10, 20]  # Bronze, Silver, Gold
        achievement_name = "Why Do We Fall"
        username = self.username

        if total_deaths >= thresholds[2]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.GOLD)
        elif total_deaths >= thresholds[1]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.SILVER)
        elif total_deaths >= thresholds[0]:
            self.achievement_manager.unlock_achievement(username, achievement_name, AchievementTier.BRONZE)

    def quit_game(self):
        arcade.close_window()