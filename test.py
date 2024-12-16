import Play,GameClass,MancalaBoardClass
import random
from math import inf
# from Animation import animate
from an import a
from input import main
# from anim import a

# 2 est le computer

choose_mode = input("CHOOSE THE MODE: (COMPUTER VS COMPUTER -1- ) or (PLAYER VS COMPUTER -2- )")
if choose_mode not in ["1", "2"]:
    raise ValueError("Invalid mode selected. Please choose either '1' or '2'.")

if choose_mode == "2":
    playerside = int(input("CHOOSE THE PLAYER SIDE THAT YOU WANT TO PLAY WITH: "))
else:
    playerside = 1
    
state=MancalaBoardClass.MancalaBoard()
game=GameClass.GameClass(state,playerside)
play=Play.Play(game)
alpha = -inf
beta = inf

turn = int(input("YOU WANT TO PLAY FIRST ('-1': YES, '1': NO)"))
if turn not in [-1, 1]:
    raise ValueError("Invalid choice for turn. Please choose either '-1' or '1'.")

while not game.gameOver():
    if(turn==-1):
        if choose_mode == "2":
            possible = game.state.possibleMoves(game.playerSide[turn])
            move = main(possible)
            game.state.doMove(game.playerSide[turn], move)
            a(game.state.board)
        else:
            _, bestpit = play.MinimaxAlphaBetaPruning(game, turn, 10, alpha, beta, 2)
            print("COMPUTER I CHOOSE :"+bestpit)
            game.state.doMove(game.playerSide[turn], bestpit)
        
        turn = -turn
    else:
        _, bestpit = play.MinimaxAlphaBetaPruning(game, turn, 10, alpha, beta, 1)
        print("I CHOOSE :" + bestpit)
        game.state.doMove(game.playerSide[turn], bestpit)
        a(game.state.board)
        turn = -turn
        
print(game.findWinner())
print(state.board)
    
