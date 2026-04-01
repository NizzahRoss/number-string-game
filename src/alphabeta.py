import time
from src.game_state import GameState
from src.minimax import heuristic


def alphabeta(
    state:   GameState,
    depth:   int,
    alpha:   float,
    beta:    float,
    is_max:  bool,
    counter: dict[str, int],
) -> float:
    """
    Alpha-Beta pruning algorithm with N-ply lookahead.

    Produces identical results to Minimax but evaluates fewer nodes
    by pruning branches that cannot affect the final decision.

    Parameters
    ----------
    state   : current game state
    depth   : plies remaining
    alpha   : best score the maximiser can guarantee so far
    beta    : best score the minimiser can guarantee so far
    is_max  : True if the current player is maximising ('first')
    counter : mutable node counter — incremented on every call

    Returns
    -------
    float : evaluated score of the state
    """
    counter['nodes'] += 1

    # Base case — terminal state or depth limit reached
    if state.is_terminal() or depth == 0:
        result = state.get_result()
        if result == 'first':  return  100 + depth
        if result == 'second': return -(100 + depth)
        if result == 'draw':   return  0
        return heuristic(state)

    moves = state.get_moves()

    if is_max:
        best: float = float('-inf')
        for move in moves:
            val   = alphabeta(state.apply_move(move), depth - 1, alpha, beta, False, counter)
            best  = max(best, val)
            alpha = max(alpha, best)
            if beta <= alpha:
                break               # beta cut-off — minimiser won't allow this
        return best
    else:
        best: float = float('inf')
        for move in moves:
            val  = alphabeta(state.apply_move(move), depth - 1, alpha, beta, True, counter)
            best = min(best, val)
            beta = min(beta, best)
            if beta <= alpha:
                break               # alpha cut-off — maximiser won't allow this
        return best


def get_best_move(
    state: GameState,
    depth: int,
) -> dict[str, object]:
    """
    Find the best move for the current player using Alpha-Beta pruning.
    Identical interface to minimax.get_best_move.

    Parameters
    ----------
    state : current game state
    depth : number of plies to search

    Returns
    -------
    dict with keys:
        move     : dict   — the best move found
        nodes    : int    — total nodes evaluated
        time_ms  : float  — time taken in milliseconds
    """
    counter:   dict[str, int]  = {'nodes': 0}
    is_first:  bool            = state.turn == 'first'
    best_move: dict | None     = None
    best_val:  float           = float('-inf') if is_first else float('inf')
    t0:        float           = time.time()

    for move in state.get_moves():
        child = state.apply_move(move)
        val   = alphabeta(child, depth - 1, float('-inf'), float('inf'), not is_first, counter)

        if is_first and val > best_val:
            best_val  = val
            best_move = move
        elif not is_first and val < best_val:
            best_val  = val
            best_move = move

    return {
        'move':    best_move,
        'nodes':   counter['nodes'],
        'time_ms': (time.time() - t0) * 1000,
    }
