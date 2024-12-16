import Play,GameClass,MancalaBoardClass
import random
from math import inf
# from Animation import animate
# from an import *
import pygame # type: ignore
import time
# from input import main

# from anim import a

# 2 est le computer
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
BROWN = (139, 69, 19)
BEIGE = (245, 222, 179)
BLACK = (0, 0, 0)
PIT_RADIUS = 40
STORE_WIDTH = 60
STORE_HEIGHT = 200


# Colors

# Initialize Pygame

pygame.init()
# Create window





def draw_board(board):
    screen.fill(BEIGE)
    
    # Draw stores (Mancala pits)
    pygame.draw.rect(screen, BROWN, (50, 100, STORE_WIDTH, STORE_HEIGHT))  # P2 store
    pygame.draw.rect(screen, BROWN, (WINDOW_WIDTH - 110, 100, STORE_WIDTH, STORE_HEIGHT))  # P1 store
    
    # Draw pits
    for i in range(6):
        # P2 pits
        x = 150 + i * 100
        pygame.draw.circle(screen, BROWN, (x, 150), PIT_RADIUS)
        
        # P1 pits
        pygame.draw.circle(screen, BROWN, (x, 250), PIT_RADIUS)
    
    # Draw stones (numbers)
    font = pygame.font.Font(None, 36)
    
    # Store numbers
    text = font.render(str(board[2]), True, BLACK)
    screen.blit(text, (65, 190))
    text = font.render(str(board[1]), True, BLACK)
    screen.blit(text, (WINDOW_WIDTH - 95, 190))
    
    # Pit numbers
    # P2 pits (G through L)
    pits_p2 = ['G', 'H', 'I', 'J', 'K', 'L']
    for i in range(6):
        text = font.render(pits_p2[i]+":"+str(board[pits_p2[i]]), True, BLACK)
        screen.blit(text, (140 + i * 100, 140))
        
    # P1 pits (A through F)
    pits_p1 = ['A', 'B', 'C', 'D', 'E', 'F']
    for i in range(6):
        text = font.render(pits_p1[i]+":"+str(board[pits_p1[i]]), True, BLACK)
        screen.blit(text, (140 + i * 100, 240))
    
    pygame.display.flip()
    time.sleep(2)


def get_user_char(board):

    
    # Define buttons
    button_width = 60
    button_height = 40
    font = pygame.font.Font(None, 36)
    buttons = {}
    x_position = 100
    for key in board:
         if key != 1 and key != 2:
            buttons[str(key)] = pygame.Rect(x_position, 80, button_width, button_height)
            x_position += 70
    
    selected_char = ''
    running = True
    
    while running:
        screen.fill((255, 255, 255))
        
        # Draw buttons
        for letter, rect in buttons.items():
            pygame.draw.rect(screen, (200, 200, 200), rect)
            text = font.render(letter, True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # Show selected character
        if selected_char:
            selected_text = font.render(f"Selected: {selected_char}", True, (0, 0, 0))
            screen.blit(selected_text, (150, 140))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for letter, rect in buttons.items():
                    if rect.collidepoint(mouse_pos):
                        selected_char = letter
                        running = False
                        
    # pygame.quit()
    return selected_char

    # time.sleep(2)
    # break

    # pygame.quit()


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
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mancala Board")
while not game.gameOver():
    if(turn==-1):
        if choose_mode == "2":
            possible = game.state.possibleMoves(game.playerSide[turn])
            move = get_user_char(possible)
            game.state.doMove(game.playerSide[turn], move)
            draw_board(game.state.board)
        else:
            _, bestpit = play.MinimaxAlphaBetaPruning(game, turn, 4, alpha, beta, 2)
            print("COMPUTER I CHOOSE :"+bestpit)
            game.state.doMove(game.playerSide[turn], bestpit)
        
        turn = -turn
    else:
        _, bestpit = play.MinimaxAlphaBetaPruning(game, turn, 4, alpha, beta, 1)
        print("I CHOOSE :" + bestpit)
        game.state.doMove(game.playerSide[turn], bestpit)
        draw_board(game.state.board)
        turn = -turn
        
print(game.findWinner())
print(state.board)
    
