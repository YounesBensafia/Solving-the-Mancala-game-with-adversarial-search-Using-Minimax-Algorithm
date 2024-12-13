from queue import Full
import Play,GameClass,MancalaBoardClass
import random
from math import inf


playerside= 1
state=MancalaBoardClass.MancalaBoard()
game=GameClass.GameClass(state,playerside)
play=Play.Play(game)

# print(state.doMove(1,2))
while game.gameOver():
    # print(game.state.board)
    if(playerside==1):
        possible = game.state.possibleMoves(playerside)
        move = random.choice(possible)
        game.state.doMove(playerside, move)
        playerside = 2
    else:
        print("youn'e")
        _, bestpit = play.MinimaxAlphaBetaPruning(2, 1000, -inf, +inf)
        print(bestpit)
        game.state.doMove(playerside, bestpit)
        playerside = 1
print(game.findWinner())
print(state.board)
    