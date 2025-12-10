"""Utility functions for Battleship game."""

import csv
from typing import List, Set, Tuple

BOARD_SIZE = 10
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


def parse_coordinates(coord_str: str) -> Tuple[int, int]:
    """
    Parse a coordinate string like 'A5' or 'a5' to (row, col).
    Returns (row, col) where row is 0-9 (A-J) and col is 0-9.
    """
    coord_str = coord_str.strip().upper()
    if len(coord_str) < 2:
        raise ValueError(f"Invalid coordinate format: {coord_str}")
    
    row_char = coord_str[0]
    col_str = coord_str[1:]
    
    if row_char < 'A' or row_char > 'J':
        raise ValueError(f"Row must be A-J, got {row_char}")
    
    try:
        col = int(col_str) - 1  # 1-indexed to 0-indexed
    except ValueError:
        raise ValueError(f"Column must be numeric, got {col_str}")
    
    if col < 0 or col >= BOARD_SIZE:
        raise ValueError(f"Column must be 1-{BOARD_SIZE}, got {int(col_str)}")
    
    row = ord(row_char) - ord('A')
    return (row, col)


def format_coordinates(row: int, col: int) -> str:
    """Convert (row, col) to 'A1' format."""
    return f"{chr(ord('A') + row)}{col + 1}"


def get_ship_cells(start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Get all cells occupied by a ship from start to end coordinates."""
    r1, c1 = start
    r2, c2 = end
    
    cells = []
    if r1 == r2:  # Horizontal
        for c in range(min(c1, c2), max(c1, c2) + 1):
            cells.append((r1, c))
    elif c1 == c2:  # Vertical
        for r in range(min(r1, r2), max(r1, r2) + 1):
            cells.append((r, c1))
    else:
        raise ValueError("Ship must be horizontal or vertical")
    
    return cells


def get_adjacent_cells(cells: List[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """Get all cells adjacent to a ship (including diagonals), excluding the ship cells themselves."""
    ship_cells = set(cells)
    adjacent = set()
    for r, c in cells:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                    if (nr, nc) not in ship_cells:  # Don't include ship cells themselves
                        adjacent.add((nr, nc))
    return adjacent


def validate_ship_placement(ships: List[Tuple[Tuple[int, int], Tuple[int, int]]], final_check: bool = True) -> bool:
    """
    Validate a list of ships.
    ships is a list of ((start_row, start_col), (end_row, end_col)) tuples.
    If final_check=True, verifies exact ship count and sizes match.
    If final_check=False, only checks for overlaps and adjacency (for incremental placement).
    Returns True if valid, raises ValueError otherwise.
    """
    all_cells = set()
    
    for i, (start, end) in enumerate(ships):
        cells = set(get_ship_cells(start, end))
        ship_size = len(cells)
        
        # Check size
        if ship_size not in SHIP_SIZES:
            raise ValueError(f"Ship {i+1} has invalid size {ship_size}")
        
        # Check for overlaps with other ships
        if all_cells & cells:
            raise ValueError(f"Ship {i+1} overlaps with another ship")
        
        # Check for adjacency with other ships
        adjacent = get_adjacent_cells(list(cells))
        if all_cells & adjacent:
            raise ValueError(f"Ship {i+1} is too close to another ship")
        
        all_cells.update(cells)
    
    # Final validation: check count and sizes
    if final_check:
        if len(ships) != len(SHIP_SIZES):
            raise ValueError(f"Expected {len(SHIP_SIZES)} ships, got {len(ships)}")
        
        actual_sizes = sorted([len(get_ship_cells(s, e)) for s, e in ships])
        if actual_sizes != sorted(SHIP_SIZES):
            raise ValueError(f"Ship sizes {actual_sizes} don't match required {sorted(SHIP_SIZES)}")
    
    return True


def save_ships_to_csv(filepath: str, ships: List[Tuple[Tuple[int, int], Tuple[int, int]]]):
    """Save ships to CSV. Format: start_coord,end_coord"""
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['start', 'end', 'size'])
        for start, end in ships:
            cells = get_ship_cells(start, end)
            writer.writerow([format_coordinates(*start), format_coordinates(*end), len(cells)])


def load_ships_from_csv(filepath: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Load ships from CSV."""
    ships = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = parse_coordinates(row['start'])
            end = parse_coordinates(row['end'])
            ships.append((start, end))
    return ships
