import pygame
import sys
from MancalaBoardClass import MancalaBoard
# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
BACKGROUND_COLOR = (230, 220, 210)  # Light beige
BOARD_COLOR = (255, 0, 0)  # Black

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
    def __init__(self, game):
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Mancala Game')
        
        # Load background image
        self.background_image = pygame.image.load('mancala.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Game state
        self.board = game.state.board.values()
        print(self.board)# 6 pits for each player, initially 4 stones
        self.player_stores = [0, 0]  # Stores for each player
        self.current_player = 0  # 0 for first player, 1 for second player
        self.pit_radius = PIT_RADIUS
        self.page = 1  # Tracks current page

    def draw_button(self, text, center_pos):
        font = pygame.font.Font(None, 48)
        button_text = font.render(text, True, BUTTON_TEXT_COLOR)
        button_rect = pygame.Rect(0, 0, 400, 60)  # Increased width to 400
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

    def draw_board(self):
        # Draw background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw main board with rounded corners
        pygame.draw.rect(
            self.screen, 
            BOARD_COLOR, 
            (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), 
            border_radius=self.pit_radius
        )

        # Draw Player 1's store (left)
        pygame.draw.rect(
            self.screen, 
            STORE_COLOR, 
            (BOARD_X - STORE_WIDTH - 20, BOARD_Y + (BOARD_HEIGHT - STORE_HEIGHT) // 2, 
             STORE_WIDTH, STORE_HEIGHT),
            border_radius=self.pit_radius
        )

        # Draw Player 2's store (right)
        pygame.draw.rect(
            self.screen, 
            STORE_COLOR, 
            (BOARD_X + BOARD_WIDTH + 20, BOARD_Y + (BOARD_HEIGHT - STORE_HEIGHT) // 2, 
             STORE_WIDTH, STORE_HEIGHT),
            border_radius=self.pit_radius
        )

        # Draw pits
        for i in range(6):
            # Player 1's pits (bottom row)
            pygame.draw.circle(
                self.screen, 
                PIT_COLOR, 
                (BOARD_X + self.pit_radius + i * (self.pit_radius * 2 + PIT_SPACING), 
                 BOARD_Y + BOARD_HEIGHT - self.pit_radius - 20),
                self.pit_radius
            )
            # Player 2's pits (top row)
            pygame.draw.circle(
                self.screen, 
                PIT_COLOR, 
                (BOARD_X + self.pit_radius + i * (self.pit_radius * 2 + PIT_SPACING), 
                 BOARD_Y + self.pit_radius + 20),
                self.pit_radius
            )

        # Display stone counts in pits
        font = pygame.font.Font(None, 36)
        for i in range(6):
            # Player 1's pit stones
            text = font.render(str(self.board[i]), True, (0, 0, 0))
            self.screen.blit(
                text, 
                (BOARD_X + self.pit_radius + i * (self.pit_radius * 2 + PIT_SPACING) - 10, 
                 BOARD_Y + BOARD_HEIGHT - self.pit_radius - 40)
            )
            # Player 2's pit stones
            text = font.render(str(self.board[i+6]), True, (0, 0, 0))
            self.screen.blit(
                text, 
                (BOARD_X + self.pit_radius + i * (self.pit_radius * 2 + PIT_SPACING) - 10, 
                 BOARD_Y + self.pit_radius + 10)
            )

        # Draw back button
        return self.draw_button('Back', (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

    def run(self):
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
                        back_button = self.draw_board()
                        if back_button.collidepoint(mouse_pos):
                            self.page = 2

            if self.page == 1:
                self.draw_start_page()
            elif self.page == 2:
                self.draw_mode_selection_page()
            elif self.page == 3:
                self.draw_board()

            pygame.display.flip()
            clock.tick(30)  # 30 FPS

def main():
    game = MancalaAnimation()
    game.run()

if __name__ == "__main__":
    main()
