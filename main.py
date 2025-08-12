import src.core.play as play,src.core.gameClass as gameClass,src.core.mancalaBoardClass as mancalaBoardClass
import random
from math import inf
import pygame
import time
import yaml
import os

# Load configuration from YAML file
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'display_settings.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

# 2 est l'ordinateur
WINDOW_WIDTH = config['window']['width']
WINDOW_HEIGHT = config['window']['height']
BROWN = tuple(config['colors']['brown'])
BEIGE = tuple(config['colors']['beige'])
BLACK = tuple(config['colors']['black'])
WHITE = tuple(config['colors']['white'])
GOLD = tuple(config['colors']['gold'])
BLUE = tuple(config['colors']['blue'])
RED = tuple(config['colors']['red'])
GREEN = tuple(config['colors']['green'])
PIT_RADIUS = config['board']['pit_radius']
STORE_WIDTH = config['board']['store_width']
STORE_HEIGHT = config['board']['store_height']
MARGIN = config['board']['margin']

pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(config['window']['title'])

background_image = pygame.image.load('./images/mancala.jpg')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

background_image1 = pygame.image.load('./images/img.jpg')
background_image1 = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

def draw_board(board):
    background_image = pygame.image.load('./images/mancala.jpg')
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(background_image, (0, 0))
    background_image = pygame.image.load('./images/mancala.jpg')
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
    
    pits_p2 = ['G', 'H', 'I', 'J', 'K', 'L']
    for i in range(6):
        text = font.render(pits_p2[i]+":"+str(board[pits_p2[i]]), True, BLACK)
        screen.blit(text, (140 + i * 100, 140))
        
    pits_p1 = ['A', 'B', 'C', 'D', 'E', 'F']
    for i in range(6):
        text = font.render(pits_p1[i]+":"+str(board[pits_p1[i]]), True, BLACK)
        screen.blit(text, (140 + i * 100, 240))
    
    pygame.display.flip()
    time.sleep(1)
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

        

        for letter, (x, y) in buttons.items():
            pygame.draw.circle(screen, (0, 0, 255), (x, y), button_radius)  # Changed color to blue
            text = font.render(letter, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)
        

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


    FONT = pygame.font.Font(None, 36)

    button_width = 300
    button_height = 80
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
        
        background_image1 = pygame.image.load('./images/img.jpg')
        background_image1 = pygame.transform.scale(background_image1, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(background_image1, (0, 0))
        question_text = FONT.render(question, True, WHITE)
        screen.blit(
            question_text,
            (WINDOW_WIDTH // 2 - question_text.get_width() // 2, 50)
        )

        pygame.draw.rect(screen, GREEN, option1_button, border_radius=20)
        pygame.draw.rect(screen, RED, option2_button, border_radius=20)

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if option1_button.collidepoint(event.pos):
                    return p1  # First option selected
                elif option2_button.collidepoint(event.pos):
                    return p2  # Second option selected

        pygame.display.flip()


mode = choose_mode("Choose mode","C vs C","H vs C")
print(mode)
if mode not in ["1", "2"]:
    raise ValueError("Invalid mode selected. Please choose either '1' or '2'.")

if mode == "2":
    playerside = int(choose_mode("Choose Side","1 : =A","2 : =G"))

else:
    playerside = 1
    
state=mancalaBoardClass.MancalaBoard()
game=gameClass.GameClass(state,playerside)
play=play.Play(game)
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
            move = get_user_char(possible)
            game.state.doMove(game.playerSide[turn], move)
            draw_board(game.state.board)
        else:
            _, bestpit = play.MinimaxAlphaBetaPruning(game, turn, 5, alpha, beta, 2)
            print("COMPUTER I CHOOSE :" + bestpit)
            font = pygame.font.Font(None, 36)
            message = f"COMPUTER I CHOOSE: {bestpit}"
            text_surface = font.render(message, True, (255,0,0))
            screen.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, WINDOW_HEIGHT - text_surface.get_height() - 10))
            pygame.display.flip()
            time.sleep(1)
            game.state.doMove(game.playerSide[turn], bestpit)
            draw_board(game.state.board)
        turn = -turn
    else:
        _, bestpit = play.MinimaxAlphaBetaPruning(game, turn, 5, alpha, beta, 1)
        print("COMPUTER# CHOOSE :" + bestpit)
        font = pygame.font.Font(None, 36)
        message = f"COMPUTER# CHOOSE: {bestpit}"
        text_surface = font.render(message, True, (255, 0, 0))
        screen.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, WINDOW_HEIGHT - text_surface.get_height() - 10))
        pygame.display.flip()
        time.sleep(1)
        game.state.doMove(game.playerSide[turn], bestpit)
        draw_board(game.state.board)
        turn = -turn

draw_board(game.state.board)        
winner_text = f"Winner: {game.findWinner()}"

FONT = pygame.font.Font(None, 36)

screen.fill(BEIGE)
winner_surface = FONT.render(winner_text, True, BLACK)
screen.blit(winner_surface, (WINDOW_WIDTH // 2 - winner_surface.get_width() // 2, WINDOW_HEIGHT // 2 - 50))


pygame.display.flip()
time.sleep(5)
pygame.quit()
    
