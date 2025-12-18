import os
from src.ship_input import get_player_ships
from src.bot_generation import generate_bot_ships
from src.gameplay import GameBoard, play_game
from src.utils import save_ships_to_csv


def main():
    """Main game flow."""
    print("\n" + "="*60)
    print("WELCOME TO CLASSIC BATTLESHIP")
    print("="*60)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    
    # Player ship input
    print("\n[PHASE 1] Setting up your ships...")
    player_ships = get_player_ships()
    save_ships_to_csv('data/player_ships.csv', player_ships)
    print("Player ships saved to data/player_ships.csv\n")
    
    # Bot ship generation
    print("[PHASE 2] Generating bot ships...")
    bot_ships = generate_bot_ships()
    save_ships_to_csv('data/bot_ships.csv', bot_ships)
    print("Bot ships generated and saved to data/bot_ships.csv\n")
    
    # Create game boards
    print("[PHASE 3] Starting game...\n")
    player_board = GameBoard(player_ships)
    bot_board = GameBoard(bot_ships)
    
    # Play game
    winner = play_game(player_board, bot_board)
    
    # Save final state
    print("\n✓ Game state saved to data/game_state.csv")
    print(f"\nFinal winner: {winner.upper()}")


if __name__ == '__main__':
    main()
