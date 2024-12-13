from copy import deepcopy
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
        
    def MinimaxAlphaBetaPruning(self, player, depth, alpha, beta):  
        print("holaaa")
        if self.game.gameOver() or depth == 1: 
            bestValue = self.game.evaluate() 
            return bestValue, None
        
        print(self.game.state.possibleMoves(self.game.playerSide[player]))       
        if player == MAX: 
            bestValue = -inf 
            for pit in self.game.state.possibleMoves(self.game.playerSide[player]): 
                child_game = self.game
                child_game.state.doMove(self.game.playerSide[player], pit) 
                value, _ = Play.MinimaxAlphaBetaPruning(child_game, -player, depth-1, alpha, beta)
                if value > bestValue: 
                        bestValue = value 
                        bestPit = pit  
                        print("a")

                if bestValue >= beta:
                    print("a") 
                    break      
                if bestValue > alpha: 
                        print("a")
                        alpha = bestValue 
        else: 
            bestValue = +inf
            for pit in self.game.state.possibleMoves(self.game.playerSide[player]): 
                child_game = deepcopy(self.game)

                child_game.state.doMove(self.game.playerSide[player], pit) 
                value, _ = Play.MinimaxAlphaBetaPruning(child_game, -player, depth-1, alpha, beta)   
                if value < bestValue:
                    print("a")
                    bestValue = value 
                    bestPit = pit       
                if bestValue <= alpha: 
                    print("a")

                    break
                if bestValue < beta:
                    print("a")
 
                    beta = bestValue 
        return bestValue, bestPit
