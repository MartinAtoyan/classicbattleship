import sys
from typing import List, Tuple
from src.utils import (
    parse_coordinates, get_ship_cells, validate_ship_placement, 
    save_ships_to_csv, BOARD_SIZE, SHIP_SIZES
)


def display_ship_input_help():
    """Display help for ship input format."""
    print("\n" + "="*60)
    print("BATTLESHIP - PLACE YOUR SHIPS")
    print("="*60)
    print(f"\nBoard size: {BOARD_SIZE}x{BOARD_SIZE}")
    print(f"Required ships: {SHIP_SIZES}")
    print("\nInput format:")
    print("  Enter ships as: START_COORD END_COORD")
    print("  Example: A1 A4  (horizontal ship at A1 to A4)")
    print("  Example: B3 D3  (vertical ship at B3 to D3)")
    print("\nCoordinate format: Letter(A-J) + Number(1-10)")
    print("  A1 = top-left corner")
    print("  J10 = bottom-right corner")
    print("\nRules:")
    print("  - Ships must not touch each other (even diagonally)")
    print("  - Ships must be in a straight line (horizontal or vertical)")
    print("  - All 10 ships required")
    print("="*60 + "\n")


def get_player_ships() -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Get ship placements from player input."""
    display_ship_input_help()
    
    ships = []
    ship_count = 0
    total_ships = len(SHIP_SIZES)
    
    while ship_count < total_ships:
        try:
            user_input = input(f"Ship {ship_count + 1}/{total_ships} - Enter start and end coordinates (or 'quit'): ").strip()
            
            if user_input.lower() == 'quit':
                print("Exiting ship placement.")
                sys.exit(0)
            
            parts = user_input.split()
            if len(parts) != 2:
                print("Invalid format. Use: START_COORD END_COORD (e.g., A1 A4)")
                continue
            
            start = parse_coordinates(parts[0])
            end = parse_coordinates(parts[1])
            
            # Check if it's a valid line
            cells = get_ship_cells(start, end)
            ship_size = len(cells)
            
            # Check if size is in our allowed sizes
            if ship_size not in SHIP_SIZES:
                print(f"Invalid ship size: {ship_size}. Allowed: {sorted(set(SHIP_SIZES))}")
                continue
            
            # Check if this size is still needed
            current_sizes = [len(get_ship_cells(s, e)) for s, e in ships]
            if current_sizes.count(ship_size) >= SHIP_SIZES.count(ship_size):
                print(f"You already have {SHIP_SIZES.count(ship_size)} ship(s) of size {ship_size}")
                continue
            
            # Add ship and only validate if all 10 are placed
            ships.append((start, end))
            
            # Only validate when final ship is added
            if len(ships) == len(SHIP_SIZES):
                validate_ship_placement(ships, final_check=True)
            else:
                # For intermediate ships, just check overlaps/adjacency
                validate_ship_placement(ships, final_check=False)
            
            ship_count += 1
            print(f"Ship {ship_count} placed (size {ship_size})")
            
        except ValueError as e:
            print(f"Error: {e}")
            print("Try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            print("Try again.")
    
    print("\nAll ships placed successfully!")
    return ships


def main():
    """Main entry point for ship input."""
    ships = get_player_ships()
    save_ships_to_csv('data/player_ships.csv', ships)
    print(f"Ships saved to data/player_ships.csv")


if __name__ == '__main__':
    main()
