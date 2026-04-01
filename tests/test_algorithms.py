import pytest
from src.game_state import GameState
from src.minimax import minimax
from src.alphabeta import alpha_beta

def test_minimax_terminal():
    gs = GameState([4], points=2, bank=0)
    value, move = minimax(gs, depth=1, maximizing_player=True)
    assert value == 1.0   # first player wins
    assert move is None

def test_minimax_one_move():
    # State [1,2,3] (odd length) with first player to move.
    gs = GameState([1,2,3])
    value, move = minimax(gs, depth=1, maximizing_player=True)
    # heuristic returns 0 for all children, so best_value = 0, best_move = first move (pair 0)
    assert value == 0.0
    assert move == {'type': 'pair', 'pair_idx': 0}

def test_alpha_beta_consistency():
    # On a small tree, alpha-beta should return same value as minimax.
    gs = GameState([1,2,3])
    val_mm, move_mm = minimax(gs, depth=2, maximizing_player=True)
    val_ab, move_ab = alpha_beta(gs, depth=2)
    assert val_mm == val_ab
    assert move_mm == move_ab
