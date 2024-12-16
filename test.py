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

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mancala Board")

# Load background image
background_image = pygame.image.load('mancala.jpg')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

background_image1 = pygame.image.load('img.jpg')
background_image1 = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

def draw_board(board):
    background_image = pygame.image.load('mancala.jpg')
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(background_image, (0, 0))
    background_image = pygame.image.load('mancala.jpg')
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
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
    text = font.render("P2:"+str(board[2]), True, (255,255,255))
    screen.blit(text, (65, 190))
    text = font.render("P1:"+str(board[1]), True, (255,255,255))
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
    time.sleep(4)
def get_user_char(board):
    # Define buttons
    button_radius = 30
    font = pygame.font.Font(None, 36)
    buttons = {}
    x_position = 100
    for key in board:
        if key != 1 and key != 2:
            buttons[str(key)] = (x_position, 100)
            x_position += 70
    
    selected_char = ''
    running = True
    
    while running:
        screen.blit(background_image, (0, 0))
        # screen.fill((255, 255, 255))
        
        # Draw buttons
        for letter, (x, y) in buttons.items():
            pygame.draw.circle(screen, (0, 0, 255), (x, y), button_radius)  # Changed color to blue
            text = font.render(letter, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x, y))
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
                for letter, (x, y) in buttons.items():
                    if (mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2 <= button_radius ** 2:
                        selected_char = letter
                        running = False
                        
    return selected_char

def choose_mode( question, option1, option2, p1="1",p2="2"):

    # Set up fonts and colors
    FONT = pygame.font.Font(None, 36)
    WHITE = (255, 255, 255)
    GREEN = (34, 139, 34)
    RED = (220, 20, 60)

    # Button properties
    button_width = 300
    button_height = 80

    # Define button positions
    option1_button = pygame.Rect(
        (WINDOW_WIDTH // 2 - button_width // 2, WINDOW_HEIGHT // 2 - 120),
        (button_width, button_height)
    )
    option2_button = pygame.Rect(
        (WINDOW_WIDTH // 2 - button_width // 2, WINDOW_HEIGHT // 2 + 40),
        (button_width, button_height)
    )

    running = True

    while running:
        
        # Fill the screen with background color
        background_image1 = pygame.image.load('img.jpg')
        background_image1 = pygame.transform.scale(background_image1, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(background_image1, (0, 0))
        # Draw the question
        question_text = FONT.render(question, True, (255,255,255))
        screen.blit(
            question_text,
            (WINDOW_WIDTH // 2 - question_text.get_width() // 2, 50)
        )

        # Draw buttons
        pygame.draw.rect(screen, GREEN, option1_button, border_radius=20)
        pygame.draw.rect(screen, RED, option2_button, border_radius=20)

        # Draw button text
        option1_text = FONT.render(option1, True, WHITE)
        option2_text = FONT.render(option2, True, WHITE)

        screen.blit(
            option1_text,
            (option1_button.centerx - option1_text.get_width() // 2,
             option1_button.centery - option1_text.get_height() // 2)
        )
        screen.blit(
            option2_text,
            (option2_button.centerx - option2_text.get_width() // 2,
             option2_button.centery - option2_text.get_height() // 2)
        )

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if option1_button.collidepoint(event.pos):
                    return p1  # First option selected
                elif option2_button.collidepoint(event.pos):
                    return p2  # Second option selected

        # Update the display
        pygame.display.flip()


mode = choose_mode("Choose mode","C vs C","H vs C")
print(mode)
if mode not in ["1", "2"]:
    raise ValueError("Invalid mode selected. Please choose either '1' or '2'.")

if mode == "2":
    playerside = int(choose_mode("Choose Side","1 : =A","2 : =G"))
    # print(playerside)

else:
    playerside = 1
    
state=MancalaBoardClass.MancalaBoard()
game=GameClass.GameClass(state,playerside)
play=Play.Play(game)
alpha = -inf
beta = inf
if mode == "2":
    turn = choose_mode("Start First ? ","YES: -1","NON: +1",-1,1)
    # h1 = 1
else:
    # h1 = 2
    turn = -1

if turn not in [-1, 1]:
    raise ValueError("Invalid choice for turn. Please choose either '-1' or '1'.")

while not game.gameOver():
    if(turn==-1):
        if mode == "2":
            possible = game.state.possibleMoves(game.playerSide[turn])
            # print("let us choose")
            move = get_user_char(possible)
            game.state.doMove(game.playerSide[turn], move)
        else:
            _, bestpit = play.MinimaxAlphaBetaPruning(game, turn, 5, alpha, beta, 2)
            print("COMPUTER I CHOOSE :" + bestpit)
            game.state.doMove(game.playerSide[turn], bestpit)
            draw_board(game.state.board)
        turn = -turn
    else:
        _, bestpit = play.MinimaxAlphaBetaPruning(game, turn, 5, alpha, beta, 1)
        print("COMPUTER# CHOOSE :" + bestpit)
        game.state.doMove(game.playerSide[turn], bestpit)
        draw_board(game.state.board)
        turn = -turn

draw_board(game.state.board)        
winner_text = f"Winner: {game.findWinner()}"

FONT = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)

screen.fill(BEIGE)
winner_surface = FONT.render(winner_text, True, BLACK)
screen.blit(winner_surface, (WINDOW_WIDTH // 2 - winner_surface.get_width() // 2, WINDOW_HEIGHT // 2 - 50))

# Display the final board state
# final_board_surface = FONT.render(final_board_text, True, BLACK)
# screen.blit(final_board_surface, (WINDOW_WIDTH // 2 - final_board_surface.get_width() // 2, WINDOW_HEIGHT // 2 + 10))

pygame.display.flip()
time.sleep(5)
pygame.quit()
    
