import Play,GameClass,MancalaBoardClass
import random
from math import inf
# from Animation import animate

# 2 est le computer

playerside= 1
state=MancalaBoardClass.MancalaBoard()
game=GameClass.GameClass(state,playerside)
play=Play.Play(game)
# animation = a

alpha = -inf
beta = inf

# print(state.doMove(1,2))
while not game.gameOver():
    # print(game.state.board)
    if(playerside==1):
        possible = game.state.possibleMoves(playerside)
        move = random.choice(possible)
        # move = input("choose a move: from "+str(possible))
        game.state.doMove(playerside, move)
        print(game.state.board)
        playerside = 2
    else:
        print("DALTIII")
        _, bestpit = play.MinimaxAlphaBetaPruning(game,playerside, 3, alpha, beta)
        
        print(bestpit)
        game.state.doMove(playerside, bestpit)
        print(game.state.board)
        playerside = 1
print(game.findWinner())
print(state.board)
    