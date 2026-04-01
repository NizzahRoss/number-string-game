import pytest
from src.game_state import GameState

def test_initial_state():
    gs = GameState([1,2,3,4])
    assert gs.nums == [1,2,3,4]
    assert gs.points == 0
    assert gs.bank == 0
    assert gs.turn == 'first'

def test_random_initial():
    gs = GameState.random_initial(20)
    assert len(gs.nums) == 20
    assert all(1 <= n <= 6 for n in gs.nums)

def test_get_moves_even():
    gs = GameState([1,2,3,4])
    moves = gs.get_moves()
    assert moves == [{'type': 'pair', 'pair_idx': 0}, {'type': 'pair', 'pair_idx': 1}]

def test_get_moves_odd():
    gs = GameState([1,2,3])
    moves = gs.get_moves()
    assert moves == [{'type': 'pair', 'pair_idx': 0}, {'type': 'delete'}]

def test_apply_pair_no_substitution():
    gs = GameState([1,2,3,4])
    new = gs.apply_move({'type': 'pair', 'pair_idx': 0})
    assert new.nums == [3,3,4]
    assert new.points == 1
    assert new.bank == 0
    assert new.turn == 'second'

def test_apply_pair_with_substitution():
    gs = GameState([5,6,1])
    new = gs.apply_move({'type': 'pair', 'pair_idx': 0})
    assert new.nums == [5,1]
    assert new.points == 1
    assert new.bank == 1
    assert new.turn == 'second'

def test_apply_delete():
    gs = GameState([1,2,3])
    new = gs.apply_move({'type': 'delete'})
    assert new.nums == [1,2]
    assert new.points == -1
    assert new.bank == 0
    assert new.turn == 'second'

def test_is_terminal():
    assert GameState([4]).is_terminal()
    assert not GameState([1,2]).is_terminal()

def test_get_result():
    # first player win: final even & total even
    gs = GameState([4], points=2, bank=0)
    assert gs.get_result() == 'first'
    # second player win: final odd & total odd
    gs = GameState([3], points=1, bank=2)  # total=3 odd
    assert gs.get_result() == 'second'
    # draw
    gs = GameState([2], points=1, bank=0)  # total=1 odd, final even
    assert gs.get_result() == 'draw'
