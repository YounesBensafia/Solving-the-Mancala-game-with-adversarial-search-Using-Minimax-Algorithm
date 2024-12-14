from copy import deepcopy
from math import inf

MAX = 2
MIN = 1

class Play:
    def __init__(self, game):
        self.game = game

    def humanTurn(self):
        valid_move = False
        while not valid_move:
            try:
                move = int(input("Choose (1-6): ")) - 1 # CHOOSE
                if move in self.game.state.possibleMoves():
                    self.game.state.doMove(1, move)
                    valid_move = True
            except ValueError:
                print("Invalid input")

    def computerTurn(self):
        move = Play.MinimaxAlphaBetaPruning(self.game)
        self.game.doMove(2, move)
        print(f"Computer chose move {move + 1}")
        
    def MinimaxAlphaBetaPruning(self, game, player, depth, alpha, beta):
        # Debugging: Print current game state and depth
        # print("Board State:", game.state.board)
        if game.gameOver() or depth == 1:  # Adjust depth exit condition
            bestValue = self.game.evaluate()
            return bestValue, None

        if player == MAX:
            bestValue = -float('inf')
            # bestPit = None
            for pit in game.state.possibleMoves(game.playerSide[player]):
                child_game = deepcopy(game)  # Correctly create a deep copy
    
                self.game.state.doMove(game.playerSide[player], pit)
                value, _ = self.MinimaxAlphaBetaPruning(child_game, MIN, depth - 1, alpha, beta)

                if value > bestValue:
                    bestValue = value
                    bestPit = pit
                if bestValue >= beta:
                    break
                if bestValue > alpha:
                    alpha = bestValue
        else:
            bestValue = float('inf')
            bestPit = None
            for pit in game.state.possibleMoves(game.playerSide[player]):
                child_game = deepcopy(game)  # Correctly create a deep copy
                child_game.state.doMove(game.playerSide[player], pit)
                value, _ = self.MinimaxAlphaBetaPruning(child_game, MAX, depth - 1, alpha, beta)

                if value < bestValue:
                    bestValue = value
                    bestPit = pit
                if bestValue <= alpha:
                    break
                if bestValue < beta:
                    beta = bestValue
        # print("best pit is " + str(bestPit))
        return bestValue, bestPit

