import pygame # type: ignore
import time

def animate_mancala_board(board_dict):
    """
    Animates a Mancala board using Pygame
    """
    # Initialize Pygame
    pygame.init()
    
    # Constants
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 400
    PIT_RADIUS = 40
    STORE_WIDTH = 60
    STORE_HEIGHT = 200
    
    # Colors
    BROWN = (139, 69, 19)
    BEIGE = (245, 222, 179)
    BLACK = (0, 0, 0)
    
    # Create window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Mancala Board")
    
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
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        draw_board(board_dict)
        # time.sleep(2)
        # break
    
    # pygame.quit()

# Example usage:
def a(example_board):    
    animate_mancala_board(example_board)
    pygame.quit()
    
