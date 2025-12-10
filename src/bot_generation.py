import random
from typing import List, Tuple
from src.utils import (
    get_ship_cells, get_adjacent_cells, validate_ship_placement,
    save_ships_to_csv, BOARD_SIZE, SHIP_SIZES)


def generate_bot_ships(max_attempts: int = 1000) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    # Generate a valid random ship placement for the bot.
    for attempt in range(max_attempts):
        ships = []
        all_cells = set()
        all_adjacent = set()
        valid = True
        
        for ship_size in SHIP_SIZES:
            placed = False
            attempts = 0
            max_placement_attempts = 100
            
            while not placed and attempts < max_placement_attempts:
                attempts += 1
                
                # Random orientation
                horizontal = random.choice([True, False])
                
                if horizontal:
                    row = random.randint(0, BOARD_SIZE - 1)
                    col = random.randint(0, BOARD_SIZE - ship_size)
                    start = (row, col)
                    end = (row, col + ship_size - 1)
                else:
                    row = random.randint(0, BOARD_SIZE - ship_size)
                    col = random.randint(0, BOARD_SIZE - 1)
                    start = (row, col)
                    end = (row + ship_size - 1, col)
                
                cells = get_ship_cells(start, end)
                adjacent = get_adjacent_cells(cells)
                
                # Check for overlaps and adjacency
                if not (all_cells & set(cells)) and not (all_adjacent & adjacent):
                    ships.append((start, end))
                    all_cells.update(cells)
                    all_adjacent.update(adjacent)
                    placed = True
            
            if not placed:
                valid = False
                break
        
        if valid:
            try:
                validate_ship_placement(ships)
                return ships
            except ValueError:
                continue
    
    raise RuntimeError(f"Failed to generate valid bot ships after {max_attempts} attempts")


def main():
    ships = generate_bot_ships()
    save_ships_to_csv('data/bot_ships.csv', ships)


if __name__ == '__main__':
    main()
