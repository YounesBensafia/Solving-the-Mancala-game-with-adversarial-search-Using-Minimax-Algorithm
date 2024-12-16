import math
import copy
def minimaxAlphaBetaPruning(game, player, depth, alpha, beta):
    if game.gameOver() or depth == 1:
        return game.evaluate(), None

    if player == 1:  # Maximizing for Computer
        best_value = -math.inf
        best_pit = None
        for pit in game.state.possibleMoves(game.playerSide[player]):
            child_game = copy.deepcopy(game)
            child_game.state.doMove(game.playerSide[player], pit)
            value, _ = minimaxAlphaBetaPruning(
                child_game, -player, depth - 1, alpha, beta
            )
            if value > best_value:
                best_value = value
                best_pit = pit
            if best_value >= beta:
                break
            if best_value > alpha:
                alpha = best_value
    else:  
        best_value = math.inf
        best_pit = None
        for pit in game.state.possibleMoves(game.playerSide[player]):
            child_game = copy.deepcopy(game)
            child_game.state.doMove(game.playerSide[player], pit)
            value, _ = minimaxAlphaBetaPruning(
                child_game, -player, depth - 1, alpha, beta
            )
            if value < best_value:
                best_value = value
                best_pit = pit
            if best_value <= alpha:
                break
            if best_value < beta:
                beta = best_value
    return best_value, best_pit