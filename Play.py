import copy
from math import inf

MAX = 1
MIN = -1

class Play:
    def __init__(self, game):
        self.game = game

    def humanTurn(self):
        valid_move = False
        while not valid_move:
            try:
                move = int(input("Enter your move (1-6): ")) - 1
                if move in self.game.state.possibleMoves():
                    self.game.state.doMove(1, move)
                    valid_move = True
            except ValueError:
                print("Invalid input")

    def computerTurn(self):
        move = Play.MinimaxAlphaBetaPruning(self.game)
        self.game.make_move(move)
        print(f"Computer chose move {move + 1}")
        
    def MinimaxAlphaBetaPruning(game, player, depth, alpha, beta):  
        if game.gameOver() or depth == 1: 
            bestValue = game.evaluate() 
            return bestValue, None 
        if player == MAX: 
            bestValue = -inf 
            for pit in game.state.possibleMoves(game.playerSide[player]): 
                child_game = copy(game) 
                child_game.state.doMove(game.playerSide[player], pit) 
                value, _ = Play.MinimaxAlphaBetaPruning(child_game, -player, depth-1, alpha, beta)
                if value > bestValue: 
                        bestValue = value 
                        bestPit = pit       
                if bestValue >= beta: 
                    break      
                if bestValue > alpha: 
                        alpha = bestValue 
        else: 
            bestValue = +inf 
            for pit in game.state.possibleMoves(game.playerSide[player]): 
                child_game = copy(game) 
                child_game.state.doMove(game.playerSide[player], pit) 
                value, _ = Play.MinimaxAlphaBetaPruning(child_game, -player, depth-1, alpha, beta)   
                if value < bestValue: 
                        bestValue = value 
                        bestPit = pit       
                if bestValue <= alpha: 
                    break
                if bestValue < beta: 
                        beta = bestValue 
                return bestValue, bestPit
