from copy import deepcopy
from math import inf
# from an import a

MAX = 1
MIN = -1

class Play:
    def __init__(self, game):
        self.game = game
    
    def humanTurn(self):
        valid_move = False
        while not valid_move:
            try:
                move = int(input("Choose (1-6): ")) - 1
                if move in self.game.state.possibleMoves():
                    self.game.state.doMove(1, move)
                    valid_move = True
            except ValueError:
                print("Invalid input")

    def computerTurn(self):
        move = Play.MinimaxAlphaBetaPruning(self.game)
        self.game.doMove(2, move)
        print(f"Computer chose move {move + 1}")
        
    def MinimaxAlphaBetaPruning(self, game, player, depth, alpha, beta, h):
        if game.gameOver() or depth == 1:
            bestValue = game.evaluate(h)
            return bestValue, None
        
        if player == MAX:
            bestValue = -float('inf')
            for pit in game.state.possibleMoves(game.playerSide[player]):
                # print(game.state.possibleMoves(game.playerSide[player]))
                child_game = deepcopy(game)
    
                child_game.state.doMove(game.playerSide[player], pit)
                
                value, _ = self.MinimaxAlphaBetaPruning(child_game, -player, depth - 1, alpha, beta, h)
                if value > bestValue:
                    bestValue = value
                    bestPit = pit
                if bestValue >= beta:
                    break
                if bestValue > alpha:
                    alpha = bestValue
        else:
            bestValue = float('inf')
            for pit in game.state.possibleMoves(game.playerSide[player]):
                child_game = deepcopy(game)
                # print(game.state.possibleMoves(game.playerSide[player]))
                child_game.state.doMove(game.playerSide[player], pit)
                value, _ = self.MinimaxAlphaBetaPruning(child_game, -player, depth - 1, alpha, beta, h)
                if value < bestValue:
                    bestValue = value
                    bestPit = pit
                if bestValue <= alpha:
                    break
                if bestValue < beta:
                    beta = bestValue
        return bestValue, bestPit

