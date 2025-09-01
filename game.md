
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
