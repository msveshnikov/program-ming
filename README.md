## 3. Required Assets

The game requires the following asset files to be present in the same directory as `game.py`:
-   **Images:**
    -   `classroom.png` (Overworld background)
    -   `background_battle.png` (Battle screen background)
    -   `kris.png` (Player character sprite)
    -   `susie.png` (NPC sprite)
    -   `ralsei.png` (NPC sprite)
    -   `svenka.png` (Hostile NPC sprite)
-   **Sounds:**
    -   `footsteps.mp3` (Player movement sound - Note: this sound is loaded but not implemented in the main loop)
    -   `music.mp3` (Background music for the overworld)
    -   `battle.mp3` (Background music for battle mode)

## 4. Global Variables & Constants

The script uses several global variables to manage the game's state and settings.

| Variable              | Type      | Description                                                                 |
| --------------------- | --------- | --------------------------------------------------------------------------- |
| `WIDTH`               | `int`     | The width of the game window in pixels.                                     |
| `HEIGHT`              | `int`     | The height of the game window in pixels.                                    |
| `WINDOW`              | `Surface` | The main Pygame display surface where all graphics are drawn.               |
| `player_x`, `player_y`| `int`     | The current X and Y coordinates of the player character.                    |
| `player_speed`        | `int`     | The speed of the player character in pixels per frame.                      |
| `player_health`       | `int`     | The player's health points, used during battle.                             |
| `game_over`           | `bool`    | A flag that becomes `True` when the player's health reaches 0.              |
| `battle_mode`         | `bool`    | A flag that becomes `True` when the player enters combat.                   |
| `current_enemy`       | `NPC`     | A reference to the NPC object the player is currently battling.             |
| `battle_timer`        | `int`     | A cooldown timer to prevent actions from happening every frame in battle.   |
| `BATTLE_COOLDOWN`     | `int`     | The number of frames for the battle action cooldown.                        |

## 5. Class Documentation

### `NPC` Class

The `NPC` class defines the behavior and attributes of all non-player characters in the game.

## 6. Design & Refactoring Considerations

To enhance scalability and maintainability, the following design improvements should be considered for future development.

### State Management

-   **Refactor Global Variables:** The extensive use of global variables can make state management difficult. Consider encapsulating related variables into dedicated classes:
    -   A `Player` class to manage `player_x`, `player_y`, `player_speed`, `player_health`, and player-specific logic.
    -   A `Game` or `GameStateManager` class to manage application-level state like `game_over`, `battle_mode`, and `current_enemy`.
-   **Implement a Finite State Machine (FSM):** Instead of a simple `battle_mode` boolean, an FSM would provide a more robust way to manage distinct game states (e.g., `Overworld`, `Battle`, `MainMenu`, `Dialogue`, `Cutscene`). This simplifies the main game loop and makes transitions between states cleaner.

### Asset and Data Management

-   **Asset Directory Structure:** Relocate assets into organized subdirectories (e.g., `assets/images/`, `assets/sounds/`, `assets/data/`) to declutter the root folder.
-   **Resource Manager:** Implement a singleton or class responsible for loading, caching, and providing access to all game assets. This prevents redundant disk I/O and centralizes asset paths.
-   **Data-Driven Design:** The presence of `lang_en_ch1.json` suggests a data-driven approach. This should be expanded:
    -   Define NPC properties (stats, positions, sprite paths, dialogue keys) in a central JSON or YAML file.
    -   Load map layouts and object placements from an external file format (e.g., Tiled map editor `.tmx` files).

### Gameplay Systems

-   **Dialogue System:** Leverage the `lang_en_ch1.json` file to build a full-featured dialogue manager. This system should handle:
    -   Rendering text boxes and character portraits.
    -   A typewriter effect for text display.
    -   Support for branching dialogue and player choices.
    -   Easy localization by loading different language files.
-   **Turn-Based Battle System:** Evolve the current battle logic into a more structured turn-based system.
    -   Create a dedicated `Battle` class to manage the battle state, turns, and UI.
    -   Implement a command menu for the player (e.g., `Fight`, `Act`, `Item`, `Mercy`).
    -   Define enemy AI with distinct attack patterns and behaviors.

### Web Deployment

-   **Leverage `index.html`:** The `index.html` file suggests potential for a web-based version. Tools like `pygbag` can be used to compile the Pygame project into WebAssembly, allowing it to run directly in a web browser. This would make the game easily accessible and shareable.