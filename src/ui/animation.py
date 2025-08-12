import pygame
import sys

# Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
BACKGROUND_COLOR = (230, 220, 210)  # Light beige

# Mancala Board Dimensions
BOARD_WIDTH = 800
BOARD_HEIGHT = 250
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_HEIGHT) // 2

# Pit Dimensions
PIT_RADIUS = 40
PIT_SPACING = 30
STORE_WIDTH = 80
STORE_HEIGHT = 200

# Colors
PIT_COLOR = (205, 133, 63)  # Peru brown
STORE_COLOR = (160, 82, 45)  # Sienna
STONE_COLOR = (169, 169, 169)  # Dark gray
BUTTON_COLOR = (0, 128, 0)  # Green
BUTTON_TEXT_COLOR = (255, 255, 255)  # White


class MancalaAnimation:
    def __init__(self):

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Mancala Game')

        self.background_image = pygame.image.load('images/mancala.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.pit_radius = PIT_RADIUS
        self.page = 1 

    def draw_button(self, text, center_pos):
        font = pygame.font.Font(None, 48)
        button_text = font.render(text, True, BUTTON_TEXT_COLOR)
        button_rect = pygame.Rect(0, 0, 300, 60)
        button_rect.center = center_pos
        pygame.draw.rect(self.screen, BUTTON_COLOR, button_rect, border_radius=15)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
        return button_rect

    def draw_start_page(self):
        self.screen.blit(self.background_image, (0, 0))
        return self.draw_button('Start', (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def draw_mode_selection_page(self):
        self.screen.blit(self.background_image, (0, 0))
        computer_vs_computer_button = self.draw_button('Computer vs Computer', (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        player_vs_computer_button = self.draw_button('Player vs Computer', (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        back_button = self.draw_button('Back', (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        return computer_vs_computer_button, player_vs_computer_button, back_button

    def draw_board(self, board):
        
        self.screen.blit(self.background_image, (0, 0))

        pygame.draw.rect(self.screen, (255, 165, 0), (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), border_radius=20)

        for i in range(2):
            pygame.draw.rect(
                self.screen, 
                STORE_COLOR, 
                (BOARD_X - STORE_WIDTH - 20 + i*4, 
                BOARD_Y + (BOARD_HEIGHT - STORE_HEIGHT) // 2 + i*4, 
                STORE_WIDTH, STORE_HEIGHT),
                border_radius=15
            )
            pygame.draw.rect(
                self.screen, 
                STORE_COLOR, 
                (BOARD_X + BOARD_WIDTH + 20 + i*4, 
                BOARD_Y + (BOARD_HEIGHT - STORE_HEIGHT) // 2 + i*4, 
                STORE_WIDTH, STORE_HEIGHT),
                border_radius=15
            )

        total_pits_width = 6 * (self.pit_radius * 2) + 5 * PIT_SPACING
        start_x = BOARD_X + (BOARD_WIDTH - total_pits_width) // 2

        font = pygame.font.Font(None, 36)

        # Player 1 pits (A-F)
        
        pits_p1 = ['A', 'B', 'C', 'D', 'E', 'F']
        
        # Player 2 pits (G-L)
        
        pits_p2 = ['G', 'H', 'I', 'J', 'K', 'L']

        for i in range(6):

            pit_x = start_x + self.pit_radius + i * (self.pit_radius * 2 + PIT_SPACING)
            y_pos = BOARD_Y + BOARD_HEIGHT - self.pit_radius - 20
            pygame.draw.circle(self.screen, PIT_COLOR, (pit_x, y_pos), self.pit_radius)
            stone_text = font.render(str(pits_p1[i])+":"+str(board[pits_p1[i]]), True, (255, 255, 255))
            stone_text_rect = stone_text.get_rect(center=(pit_x, y_pos))
            self.screen.blit(stone_text, stone_text_rect)

            
            y_pos = BOARD_Y + self.pit_radius + 20
            pygame.draw.circle(self.screen, PIT_COLOR, (pit_x, y_pos), self.pit_radius)
            stone_text = font.render(str(pits_p2[i])+":"+str(board[pits_p2[i]]), True, (255, 255, 255))
            stone_text_rect = stone_text.get_rect(center=(pit_x, y_pos))
            self.screen.blit(stone_text, stone_text_rect)

        store_font = pygame.font.Font(None, 48)

        text = store_font.render(str(board[1]), True, (255, 255, 255))
        text_rect = text.get_rect(center=(BOARD_X - STORE_WIDTH//2 - 20, BOARD_Y + BOARD_HEIGHT//2))
        self.screen.blit(text, text_rect)
        
        text = store_font.render(str(board[2]), True, (255, 255, 255))
        text_rect = text.get_rect(center=(BOARD_X + BOARD_WIDTH + STORE_WIDTH//2 + 20, BOARD_Y + BOARD_HEIGHT//2))
        self.screen.blit(text, text_rect)

        return self.draw_button('Back', (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))

    def run(self, game):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.page == 1:  # Start page
                        start_button = self.draw_start_page()
                        if start_button.collidepoint(mouse_pos):
                            self.page = 2
                    elif self.page == 2:  # Mode selection page
                        comp_vs_comp, player_vs_comp, back_button = self.draw_mode_selection_page()
                        if comp_vs_comp.collidepoint(mouse_pos):
                            print("Computer vs Computer selected")
                            self.page = 3
                        elif player_vs_comp.collidepoint(mouse_pos):
                            print("Player vs Computer selected")
                            self.page = 3
                        elif back_button.collidepoint(mouse_pos):
                            self.page = 1
                    elif self.page == 3:  # Board page
                        back_button = self.draw_board(game)
                        if back_button.collidepoint(mouse_pos):
                            self.page = 2
            if self.page == 1:
                self.draw_start_page()
            elif self.page == 2:
                self.draw_mode_selection_page()
            elif self.page == 3:
                self.draw_board(game)
                

            pygame.display.flip()
            clock.tick(30)  # 30 FPS


def animate():
    game = MancalaAnimation()
    game.run({
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4, #PLAYER1
            
            1: 0, #STORE 1
            
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4, # PLAYER2
            
            2: 0  #STORE 2
        })
    
animate()
    
