# Horizon - 2D Action-Survival Video Game

## ***Authors***
- Andrei-Daniel BOGHICI (AndreiB2005)
- Andrei-Claudiu STRECHE (AndreiStreche0)
Link: https://github.com/AndreiStreche0/Horizon.git

## ***Description***
Horizon is a 2D Action-Survival videogame in which the player has to defeat a great variety of enemies and survive a number of waves in order to win. The player can also achieve different scores and reach a number of achievements, giving them the possibility to improve their skills and replay the game each time with different goals set in mind.

## ***Technologies used***
- **Language**: Python 3.12
- **Game Framework**: Arcade 3.3.3 - A modern Python framework for building 2D games
- **Map Format**: Tiled (.tmx files) - Used for level design and tilemap management
- **Data Format**: JSON - For storing achievements and player data
- **State Machine Architecture**: Custom state-based system for managing different game states (Menu, Play, Pause, Win, Lose, Login, Leaderboard, Achievements, Character Selection)

## ***Requirements***
- Python 3.8 or higher
- arcade library (for 2D game rendering and window management) - preferably arcade 3 or higher
- Additional dependencies for game assets and data handling

## ***Installing***
Run the following commands in your terminal:
> git clone git clone https://github.com/AndreiStreche0/Horizon.git
> cd Horizon
> python3 -m venv venv
> source venv/bin/activate
> pip install arcade
> pip install bcrypt
> python3 main.py

## ***Game Features***
Horizon is implemented with a variety of features present in multiple other games. Some noteable ones are:
- **Multiple Playable Characters**: Knight, Templar and Axeman with unique stats, animations and attack patterns
- **Enemy Variety**: 7 different enemy types (Skeleton, Orc, Armored Skeleton, Armored Orc, Werewolf, Werebear, Greatsword Skeleton)
- **Wave-Based Combat**: Progressive difficulty with enemy spawning waves
- **Achievement System**: Track player accomplishments with different tiers
- **Leaderboard**: Compare scores with other players
- **Dynamic Animation System**: Frame-based animations for player characters and enemies
- **Collision Detection**: Advanced hitbox system for combat interactions
- **Persistent Data**: Save and load player progress and achievements

## Project Structure
- `app/` - Core game logic and state management
  - `brain.py` - Main game controller
  - `entities/` - Player and enemy entity classes
  - `states/` - Game state implementations
  - `pve_logic/` - Combat, collision, and spawning mechanics
  - `ui/` - User interface components (HUD, menus, buttons)
  - `map/` - Tilemap loading and management
  - `achievements/` - Achievement system
- `assets/` - Game sprites, animations, and tilesets
- `storage/` - Data persistence (authentication, leaderboard, achievements)
- `config.py` - Game configuration and character definitions

## ***Individual work***

### Andrei-Daniel BOGHICI
- Implemented player and enemies, added animations for each one (idle, run, multiple types of attacks, taking damage, dying)
- Implemented the combat between the player and the enemies (hitbox and attack hitbox for each one)
- Created a state for choosing your own character
- Created map for the game, along with collisions that limit the player and enemies in a large, but closed area
- Fix sme of the bugs that appeared during the development of the game and during merge

### Andrei-Claudiu STRECHE
- Created the initial skeleton for the project
- Created and implemented the brain logix (switching between states, holds current game data)
- Created and implemented the states of the game and their logic: play, pause, win, lose, achievement, menu, leaderboards, login
- Implemented the spawn logic for the enemies
- Created storage data that holds data about players and their game achievements
- Created the HUD

## ***Challenges & Known Issues***

### Challenges During Development

#### Game Balance & Calibration
Finding the right balance between player and enemy stats was one of our biggest challenges. We had to carefully tune:
- Player character stats (HP, damage, speed) for each class
- Enemy stats that scale appropriately as waves progress
- Spawn timing to maintain fast-paced gameplay without overwhelming the player
- Wave difficulty progression to keep the game challenging yet enjoyable

This required extensive playtesting and manual adjustments until we achieved a sweet spot - fast enough to minimize downtime, but relaxed enough to remain enjoyable.

#### Full-Screen Implementation
We encountered critical issues when implementing full-screen mode. The full-screen toggle caused input processing to break, and despite multiple attempts to debug and fix the issue, we couldn't find a reliable solution. 

**Current Workaround**: The game uses fixed screen dimensions (1920x1080 by default), which can be easily modified by users in [config.py](config.py) by changing the `SCREEN_WIDTH` and `SCREEN_HEIGHT` values.

### Known Issues

#### Map Loading
While the map itself loads just fine, it might take a few minutes for it to load, depends on the device

#### Visual Bugs
- Occasional visual glitches may occur during state transitions
- Animation sprites may briefly flicker when switching between game states

#### Git Merge Conflicts
During development, we encountered several issues when merging branches:
- Code conflicts in state management files required careful manual resolution
- Asset file conflicts occasionally required re-importing sprites
- Configuration file merges sometimes resulted in inconsistent game balance that needed re-testing

These merge issues taught us the importance of proper version control practices and thorough testing after each merge.

### Notes
While we solved the majority of the bugs, we cannot guarantee that the game doesn't have any. During our tests, the game and all of its' features worked as planned, if any issues emerge, contact us!