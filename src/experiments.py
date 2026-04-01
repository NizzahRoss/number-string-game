import csv
import time
import random
from typing import Callable
from src.game_state import GameState
from src.minimax import minimax
from src.alphabeta import alpha_beta

def run_game(initial_state: GameState,
             move_selector: Callable[[GameState], dict],
             max_depth: int = 10) -> dict:
    """
    Run a single game using the given move selector function.
    move_selector receives the current state and returns a move dict.
    Returns a dict with game metadata.
    """
    state = initial_state.clone()
    move_history = []
    start_time = time.time()

    while not state.is_terminal():
        move = move_selector(state)
        move_history.append(move)
        state = state.apply_move(move)

    end_time = time.time()
    result = state.get_result()
    return {
        'initial_length': len(initial_state.nums),
        'initial_numbers': initial_state.nums,
        'final_number': state.nums[0],
        'total_score': state.points,
        'bank': state.bank,
        'result': result,          # 'first', 'second', or 'draw'
        'moves': move_history,
        'duration': end_time - start_time
    }

def run_experiments(initial_length: int,
                    player1_fn: Callable[[GameState], dict],
                    player2_fn: Callable[[GameState], dict],
                    num_games: int = 100,
                    max_depth: int = 10,
                    csv_filename: str = "experiments.csv") -> None:
    """
    Run multiple games between two AI functions and save results to CSV.
    player1_fn and player2_fn should be functions that take a GameState and return a move dict.
    """
    results = []
    for i in range(num_games):
        state = GameState.random_initial(initial_length)
        def selector(s):
            if s.turn == 'first':
                return player1_fn(s)
            else:
                return player2_fn(s)
        game_data = run_game(state, selector, max_depth)
        game_data['game_id'] = i
        results.append(game_data)

    # Write to CSV
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['game_id', 'initial_length', 'initial_numbers',
                                                'final_number', 'total_score', 'bank',
                                                'result', 'moves', 'duration'])
        writer.writeheader()
        for r in results:
            # Convert lists to strings for CSV
            r['initial_numbers'] = str(r['initial_numbers'])
            r['moves'] = str(r['moves'])
            writer.writerow(r)
    print(f"Experiments saved to {csv_filename}")

# Example AI move selectors (for testing)
def random_ai(state: GameState) -> dict:
    moves = state.get_moves()
    return random.choice(moves)

def minimax_ai(state: GameState, depth: int = 5) -> dict:
    _, move = minimax(state, depth, maximizing_player=(state.turn == 'first'))
    return move

def alphabeta_ai(state: GameState, depth: int = 5) -> dict:
    _, move = alpha_beta(state, depth)
    return move
