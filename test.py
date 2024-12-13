import Play,GameClass,MancalaBoardClass
import random
from math import inf

# 2 est le computer

playerside= 1
state=MancalaBoardClass.MancalaBoard()
game=GameClass.GameClass(state,playerside)
play=Play.Play(game)

alpha = -inf
beta = inf

# print(state.doMove(1,2))
while not game.gameOver():
    # print(game.state.board)
    if(playerside==1):
        possible = game.state.possibleMoves(playerside)
        print(possible)
        move = random.choice(possible)
        game.state.doMove(playerside, move)
        playerside = 2
    else:
        print("a")
        _, bestpit = play.MinimaxAlphaBetaPruning(playerside, 50, alpha, beta)
        # print(bestpit)
        # game.state.doMove(playerside, bestpit)
        playerside = 1
print(game.findWinner())
print(state.board)
    