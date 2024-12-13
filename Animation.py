import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
BACKGROUND_COLOR = (230, 220, 210)  # Light beige
BOARD_COLOR = (255, 120, 19)  # Dark brown

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
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Mancala Game')
        
        # Load background image
        self.background_image = pygame.image.load('mancala.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Game state
        self.board = [4] * 12  # 6 pits for each player, initially 4 stones
        self.player_stores = [0, 0]  # Stores for each player
        self.current_player = 0  # 0 for first player, 1 for second player
        self.pit_radius = PIT_RADIUS
        self.game_started = False

    def draw_button(self):
        font = pygame.font.Font(None, 48)
        button_text = font.render('Start', True, BUTTON_TEXT_COLOR)
        button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50))
        pygame.draw.rect(self.screen, BUTTON_COLOR, button_rect, border_radius=15)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
        return button_rect

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
        pygame.draw.rect(
            self.screen, 
            (0, 0, 0),  # Black border
            (BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT), 
            3,  # Border thickness
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
        pygame.draw.rect(
            self.screen, 
            (0, 0, 0),  # Black border
            (BOARD_X - STORE_WIDTH - 20, BOARD_Y + (BOARD_HEIGHT - STORE_HEIGHT) // 2, 
             STORE_WIDTH, STORE_HEIGHT),
            3,  # Border thickness
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
        pygame.draw.rect(
            self.screen, 
            (0, 0, 0),  # Black border
            (BOARD_X + BOARD_WIDTH + 20, BOARD_Y + (BOARD_HEIGHT - STORE_HEIGHT) // 2, 
             STORE_WIDTH, STORE_HEIGHT),
            3,  # Border thickness
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
            pygame.draw.circle(
                self.screen, 
                (0, 0, 0),  # Black border
                (BOARD_X + self.pit_radius + i * (self.pit_radius * 2 + PIT_SPACING), 
                 BOARD_Y + BOARD_HEIGHT - self.pit_radius - 20),
                self.pit_radius,
                3  # Border thickness
            )
            # Player 2's pits (top row)
            pygame.draw.circle(
                self.screen, 
                PIT_COLOR, 
                (BOARD_X + self.pit_radius + i * (self.pit_radius * 2 + PIT_SPACING), 
                 BOARD_Y + self.pit_radius + 20),
                self.pit_radius
            )
            pygame.draw.circle(
                self.screen, 
                (0, 0, 0),  # Black border
                (BOARD_X + self.pit_radius + i * (self.pit_radius * 2 + PIT_SPACING), 
                 BOARD_Y + self.pit_radius + 20),
                self.pit_radius,
                3  # Border thickness
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

        # Display store counts
        font = pygame.font.Font(None, 48)
        p1_store_text = font.render(str(self.player_stores[0]), True, (255, 255, 255))
        p2_store_text = font.render(str(self.player_stores[1]), True, (255, 255, 255))
        self.screen.blit(
            p1_store_text, 
            (BOARD_X - STORE_WIDTH // 2 - 20, BOARD_Y + BOARD_HEIGHT // 2 - 24)
        )
        self.screen.blit(
            p2_store_text, 
            (BOARD_X + BOARD_WIDTH + STORE_WIDTH // 2 + 20, BOARD_Y + BOARD_HEIGHT // 2 - 24)
        )

    def set_pit_radius(self, radius):
        self.pit_radius = radius

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_started:
                    mouse_pos = event.pos
                    button_rect = self.draw_button()
                    if button_rect.collidepoint(mouse_pos):
                        self.game_started = True

            if self.game_started:
                self.draw_board()
            else:
                self.screen.blit(self.background_image, (0, 0))
                self.draw_button()

            pygame.display.flip()
            clock.tick(30)  # 30 FPS
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

                # Draw pits with a more modern design
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

                # Display stone counts in pits with a more modern font
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

                # Display store counts with a more modern font
                font = pygame.font.Font(None, 48)
                p1_store_text = font.render(str(self.player_stores[0]), True, (255, 255, 255))
                p2_store_text = font.render(str(self.player_stores[1]), True, (255, 255, 255))
                
                self.screen.blit(
                    p1_store_text, 
                    (BOARD_X - STORE_WIDTH // 2 - 20, BOARD_Y + BOARD_HEIGHT // 2 - 24)
                )
                self.screen.blit(
                    p2_store_text, 
                    (BOARD_X + BOARD_WIDTH + STORE_WIDTH // 2 + 20, BOARD_Y + BOARD_HEIGHT // 2 - 24)
                )

def main():
    game = MancalaAnimation()
    game.set_pit_radius(50)  # Example of setting a new radius
    game.run()

if __name__ == "__main__":
    main()

