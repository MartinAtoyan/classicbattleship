# Classic Battleship Game

## Game Overview

- **Board Size:** 10×10 (coordinates A-J, 1-10)
- **Ship Configuration:**
  - 1 ship of size 4
  - 2 ships of size 3
  - 3 ships of size 2
  - 4 ships of size 1
- **Rules:** Ships cannot touch each other, even diagonally

## Installation & Setup

### Requirements
- Python 3.7 or higher
- matplotlib>=3.5.0
- numpy>=1.20.0


### Quick Start

```bash
# Navigate to project directory
cd /path/to/classicbattleship

# Run the game
python3 main.py
```

## How to Play

### 1. **Player Ship Placement**
When the game starts, you'll be prompted to place your 10 ships on the board.

**Input Format:** `START_COORD END_COORD`
- Example: `A1 A4` (horizontal ship from A1 to A4)
- Example: `B3 D3` (vertical ship from B3 to D3)
- Coordinates: Letter (A-J) + Number (1-10)

**Validation:**
- Ships must be in a straight line (horizontal or vertical)
- Ships must not overlap
- Ships must not touch each other diagonally
- Ship sizes must match the required configuration

### 2. **Bot Ship Generation**
The bot automatically generates a valid random ship layout using the same rules.

### 3. **Gameplay**
Players take turns:
1. **Your Turn:** Enter a coordinate to fire (e.g., `A5`)
2. **Bot's Turn:** The bot fires at a random location
3. **Game Display:** After each move, both boards are displayed:
   - `X` = Hit
   - `O` = Miss (or auto-marked zone around destroyed ship)
   - `.` = Unknown
   - `S` = Your ship (visible only on your board)

### 4. **Ship Destruction**
When a ship is fully destroyed:
- All 8 surrounding cells are automatically marked as misses
- These marks are saved to the game state CSV

### 5. **Victory**
The game ends when one player destroys all opponent's ships.

## File Structure

```
classicbattleship/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies (none needed)
├── README.md              # This file
├── src/
│   ├── ship_input.py      # Player ship placement & validation
│   ├── bot_generation.py  # Random bot ship generation
│   ├── gameplay.py        # Game loop & board display
│   └── utils.py           # Utilities (coordinates, validation, CSV I/O)
├── data/
│   ├── player_ships.csv   # Player's ship positions
│   ├── bot_ships.csv      # Bot's ship positions
│   └── game_state.csv     # Move history (turn, coordinates, hits/misses)
└── outputs/               # Reserved for additional logs
```

## Data Formats

### Ship CSV Format (`player_ships.csv`, `bot_ships.csv`)
```
start,end,size
A1,A4,4
B3,B5,3
C7,C8,2
...
```

### Game State CSV Format (`game_state.csv`)
```
turn,player_move,player_hit,bot_move,bot_hit
1,A5,miss,D3,miss
2,B6,hit,C4,miss
3,B7,hit,C5,hit
...
```