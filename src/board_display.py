import matplotlib
matplotlib.use('Qt5Agg') 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Tuple, Set
from src.utils import BOARD_SIZE


class MatplotlibBoardDisplay:
    
    CELL_SIZE = 0.5
    COLORS = {
        'water': '#4A90E2',      # Blue
        'unknown': '#E8E8E8',    # Light gray
        'hit': '#E74C3C',        # Red
        'miss': '#95A5A6',       # Gray
        'ship': '#F39C12',       # Orange
        'destroyed_zone': '#95A5A6'  # Gray (same as miss)
    }
    
    def __init__(self):
        self.fig = None
        self.axes = None
    
    def create_figure(self, title: str = "Battleship Game"):
        self.fig, self.axes = plt.subplots(1, 2, figsize=(14, 7))
        self.fig.suptitle(title, fontsize=16, fontweight='bold')
        return self.fig
    
    def draw_board(self, ax, hits: Set[Tuple[int, int]], misses: Set[Tuple[int, int]],
                   destroyed_zones: Set[Tuple[int, int]], ships: Set[Tuple[int, int]] = None,
                   board_label: str = "Board", show_ships: bool = False):
        """
        Args:
            ax: matplotlib axis to draw on
            hits: set of (row, col) that are hits
            misses: set of (row, col) that are misses
            destroyed_zones: set of (row, col) that are destroyed zones
            ships: set of (row, col) that contain ships
            board_label: label for the board
            show_ships: whether to show ship positions
        """
        ax.set_xlim(-0.5, BOARD_SIZE - 0.5)
        ax.set_ylim(-0.5, BOARD_SIZE - 0.5)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        
        # Set labels
        ax.set_xticks(range(BOARD_SIZE))
        ax.set_xticklabels([str(i + 1) for i in range(BOARD_SIZE)])
        ax.set_yticks(range(BOARD_SIZE))
        ax.set_yticklabels([chr(ord('A') + i) for i in range(BOARD_SIZE)])
        ax.set_xlabel('Column')
        ax.set_ylabel('Row')
        ax.set_title(board_label, fontsize=12, fontweight='bold')
        
        # Draw grid
        for i in range(BOARD_SIZE + 1):
            ax.axhline(i - 0.5, color='black', linewidth=0.5)
            ax.axvline(i - 0.5, color='black', linewidth=0.5)
        
        # Draw cells
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cell = (r, c)
                
                if cell in hits:
                    color = self.COLORS['hit']
                    symbol = '✕'
                elif cell in misses or cell in destroyed_zones:
                    color = self.COLORS['miss']
                    symbol = '○'
                elif show_ships and ships and cell in ships:
                    color = self.COLORS['ship']
                    symbol = '■'
                else:
                    color = self.COLORS['unknown']
                    symbol = ''
                
                # Draw rectangle
                rect = patches.Rectangle(
                    (c - 0.4, r - 0.4), 0.8, 0.8,
                    linewidth=0, facecolor=color, edgecolor='black'
                )
                ax.add_patch(rect)
                
                # Add symbol text
                if symbol:
                    ax.text(c, r, symbol, ha='center', va='center',
                           fontsize=12, fontweight='bold', color='white')
        
        ax.set_aspect('equal')
    
    def display_game_state(self, player_hits: Set[Tuple[int, int]], 
                          player_misses: Set[Tuple[int, int]],
                          player_destroyed_zones: Set[Tuple[int, int]],
                          player_ships: Set[Tuple[int, int]],
                          bot_hits: Set[Tuple[int, int]],
                          bot_misses: Set[Tuple[int, int]],
                          bot_destroyed_zones: Set[Tuple[int, int]],
                          turn: int = 0):
        """
        Args:
            player_hits, player_misses, player_destroyed_zones: player's board state
            player_ships: player's ship positions
            bot_hits, bot_misses, bot_destroyed_zones: bot's board state (from player's perspective)
            turn: current turn number
        """
        self.create_figure(f"Battleship Game - Turn {turn}")
        
        # Draw player's board (with ships visible)
        self.draw_board(
            self.axes[0],
            hits=player_hits,
            misses=player_misses,
            destroyed_zones=player_destroyed_zones,
            ships=player_ships,
            board_label="Your Board (Your Ships)",
            show_ships=True
        )
        
        # Draw enemy's board (without ships)
        self.draw_board(
            self.axes[1],
            hits=bot_hits,
            misses=bot_misses,
            destroyed_zones=bot_destroyed_zones,
            ships=None,
            board_label="Enemy Board (What You Know)",
            show_ships=False
        )
        
        plt.tight_layout()
        return self.fig
    
    def show(self):
        """Display the current figure."""
        if self.fig:
            plt.show()
    
    def save(self, filepath: str):
        """Save the current figure to a file."""
        if self.fig:
            self.fig.savefig(filepath, dpi=100, bbox_inches='tight')
            print(f"Board saved to {filepath}")
    
    def close(self):
        """Close the figure."""
        if self.fig:
            plt.close(self.fig)
            self.fig = None
            self.axes = None


def display_boards(player_board, bot_board, turn: int = 0, save_to: str = None):
    """
    Convenience function to display both boards.
    
    Args:
        player_board: GameBoard instance (player's board)
        bot_board: GameBoard instance (bot's board)
        turn: current turn number
        save_to: optional filepath to save the figure
    """
    display = MatplotlibBoardDisplay()
    
    display.display_game_state(
        player_hits=player_board.hits,
        player_misses=player_board.misses,
        player_destroyed_zones=player_board.destroyed_zones,
        player_ships=player_board.ship_cells,
        bot_hits=bot_board.hits,
        bot_misses=bot_board.misses,
        bot_destroyed_zones=bot_board.destroyed_zones,
        turn=turn
    )
    
    if save_to:
        display.save(save_to)
    
    display.show()
    display.close()
