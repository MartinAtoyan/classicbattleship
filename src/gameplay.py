import csv
from typing import List, Tuple, Set, Dict
from src.board_display import display_boards
from src.utils import (
    parse_coordinates, format_coordinates, get_ship_cells, get_adjacent_cells,
    BOARD_SIZE)



class GameBoard:
    
    def __init__(self, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]):
        """Initialize board with ships."""
        self.ships = ships
        self.ship_cells: Set[Tuple[int, int]] = set()
        for start, end in ships:
            self.ship_cells.update(get_ship_cells(start, end))
        
        # Board state: None = unknown, True = hit, False = miss
        self.hits: Set[Tuple[int, int]] = set()
        self.misses: Set[Tuple[int, int]] = set()
        self.destroyed_zones: Set[Tuple[int, int]] = set()
    
    def get_cell_state(self, row: int, col: int) -> str:
        """Get the visual representation of a cell."""
        cell = (row, col)
        if cell in self.hits:
            return 'X'  
        elif cell in self.misses or cell in self.destroyed_zones:
            return 'O'  
        else:
            return '.'  # Unknown
    
    def record_shot(self, row: int, col: int) -> bool:
        """
        Record a shot at (row, col).
        Returns True - hit, False - miss.
        ValueError if cell already shot.
        """
        cell = (row, col)
        if cell in self.hits or cell in self.misses or cell in self.destroyed_zones:
            raise ValueError(f"Cell {format_coordinates(row, col)} already shot")
        
        if cell in self.ship_cells:
            self.hits.add(cell)
            self._check_destroyed_ships()
            return True
        else:
            self.misses.add(cell)
            return False
    
    def _check_destroyed_ships(self):
        """Check if any ships are destroyed and mark surrounding cells."""
        for start, end in self.ships:
            cells = set(get_ship_cells(start, end))
            if cells.issubset(self.hits):
                # Ship destroyed, mark adjacent cells as misses
                adjacent = get_adjacent_cells(list(cells))
                self.destroyed_zones.update(adjacent - cells)
    
    def has_ships_remaining(self) -> bool:
        """Check if any ships are still floating."""
        for start, end in self.ships:
            cells = set(get_ship_cells(start, end))
            if not cells.issubset(self.hits):
                return True
        return False


class GameState:
    """Manages the overall game state and CSV logging."""
    
    def __init__(self, player_board: GameBoard, bot_board: GameBoard):
        self.player_board = player_board
        self.bot_board = bot_board
        self.turn = 0
        self.move_history: List[Dict] = []
    
    def log_move(self, turn: int, player_coord: str, player_hit: bool,
                 bot_coord: str, bot_hit: bool):
        """Log a move to the move history."""
        self.move_history.append({
            'turn': turn,
            'player_move': player_coord,
            'player_hit': 'hit' if player_hit else 'miss',
            'bot_move': bot_coord,
            'bot_hit': 'hit' if bot_hit else 'miss'
        })
    
    def save_to_csv(self, filepath: str):
        """Save game state to CSV."""
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['turn', 'player_move', 'player_hit', 'bot_move', 'bot_hit'])
            writer.writeheader()
            writer.writerows(self.move_history)


def display_game_state(game_state: GameState, save_figure: bool = False):
    """Display both boards using matplotlib."""
    filename = None
    if save_figure:
        filename = f'outputs/turn_{game_state.turn:03d}.png'
    
    display_boards(
        game_state.player_board,
        game_state.bot_board,
        turn=game_state.turn,
        save_to=filename
    )


def get_player_move() -> Tuple[int, int]:
    """Get a valid move from the player."""
    while True:
        try:
            coord = input("Enter your shot coordinate (e.g., A1): ").strip().upper()
            row, col = parse_coordinates(coord)
            return (row, col)
        except ValueError as e:
            print(f"Invalid coordinate: {e}")


def play_game(player_board: GameBoard, bot_board: GameBoard):
    """Main game loop."""
    game_state = GameState(player_board, bot_board)
    
    print("\n" + "="*60)
    print("BATTLESHIP GAME STARTED!")
    print("="*60)
    print("Visual boards will be displayed after each turn.")
    print()
    
    while True:
        game_state.turn += 1
        print(f"\n--- TURN {game_state.turn} ---")
        
        # Display board
        display_game_state(game_state, save_figure=True)
        
        # Player move
        print("\nYOUR TURN:")
        while True:
            try:
                row, col = get_player_move()
                player_hit = bot_board.record_shot(row, col)
                player_move_str = format_coordinates(row, col)
                print(f"You shot at {player_move_str}: {'HIT!' if player_hit else 'Miss.'}")
                break
            except ValueError as e:
                print(f"Invalid move: {e}")
        
        if not bot_board.has_ships_remaining():
            print("\n🎉 YOU WIN! All enemy ships destroyed!")
            game_state.log_move(game_state.turn, player_move_str, player_hit, '', False)
            game_state.save_to_csv('data/game_state.csv')
            display_game_state(game_state, save_figure=True)
            return 'player'
        
        # Bot move (random for now, will be enhanced)
        print("\nBOT'S TURN:")
        import random
        while True:
            row = random.randint(0, BOARD_SIZE - 1)
            col = random.randint(0, BOARD_SIZE - 1)
            try:
                bot_hit = player_board.record_shot(row, col)
                bot_move_str = format_coordinates(row, col)
                print(f"Bot shot at {bot_move_str}: {'HIT!' if bot_hit else 'Miss.'}")
                break
            except ValueError:
                continue
        
        if not player_board.has_ships_remaining():
            print("\n💀 YOU LOSE! All your ships destroyed!")
            game_state.log_move(game_state.turn, player_move_str, player_hit, bot_move_str, bot_hit)
            game_state.save_to_csv('data/game_state.csv')
            display_game_state(game_state, save_figure=True)
            return 'bot'
        
        game_state.log_move(game_state.turn, player_move_str, player_hit, bot_move_str, bot_hit)
