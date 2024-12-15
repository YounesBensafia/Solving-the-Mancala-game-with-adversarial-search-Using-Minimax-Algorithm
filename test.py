import Play,GameClass,MancalaBoardClass
import random
from math import inf
# from Animation import run, MancalaAnimation
from an import a
# 2 est le computer

playerside= 1
state=MancalaBoardClass.MancalaBoard()
game=GameClass.GameClass(state,playerside)
play=Play.Play(game)
alpha = -inf
beta = inf
turn = 1 
# animate(game.state.board)

while not game.gameOver():
    # print(game.state.board)
    if(turn==1):
        # print(game.playerSide[turn])
        possible = game.state.possibleMoves(game.playerSide[turn])
        # move = random.choice(possible)
        move = input("choose a move: from " + str(possible)+ " ")
        game.state.doMove(game.playerSide[playerside], move)
        a(game.state.board)
        # animate(game.state.board)
        turn = 2
        # a(game.state.board)
    else:
        _, bestpit = play.MinimaxAlphaBetaPruning(game, game.playerSide[turn], 3, alpha, beta)
        print(bestpit)
        game.state.doMove(game.playerSide[turn], bestpit)
        a(game.state.board)

        # a(game.state.board)
        turn = 1
print(game.findWinner())
print(state.board)
    
