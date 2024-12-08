import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mancala Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (102, 51, 0)
LIGHT_BROWN = (153, 102, 51)
STONE_COLOR = (200, 100, 50)
HIGHLIGHT = (255, 255, 0)

# Fonts
pygame.font.init()
FONT = pygame.font.Font(pygame.font.get_default_font(), 24)

# Board Layout
PIT_RADIUS = 50
STONE_RADIUS = 12
PIT_POSITIONS = [
    # Top row (Player 2 side)
    (150 + i * 120, 150) for i in range(6)
] + [
    # Bottom row (Player 1 side)
    (150 + i * 120, 350) for i in range(6)
]
STORE_POSITIONS = [(50, 250), (950, 250)]  # Left and right stores

# Stone count in each pit (default setup)
stones = [4] * 6 + [0] + [4] * 6 + [0]


def draw_board():
    """Draw the Mancala board and pits."""
    # Background
    screen.fill((34, 139, 34))  # Grass green background
    pygame.draw.rect(screen, LIGHT_BROWN, (100, 100, 800, 300), border_radius=20)  # Board
    
    # Draw pits
    for i, pos in enumerate(PIT_POSITIONS):
        color = HIGHLIGHT if stones[i] > 0 else BROWN
        pygame.draw.circle(screen, color, pos, PIT_RADIUS)
        pygame.draw.circle(screen, BLACK, pos, PIT_RADIUS, 3)  # Outline

    # Draw stores
    for i, pos in enumerate(STORE_POSITIONS):
        pygame.draw.rect(screen, BROWN, (pos[0] - 40, pos[1] - 100, 80, 200), border_radius=20)
        pygame.draw.rect(screen, BLACK, (pos[0] - 40, pos[1] - 100, 80, 200), 3, border_radius=20)  # Outline

    # Add labels
    player1_label = FONT.render("Player 1", True, BLACK)
    player2_label = FONT.render("Player 2", True, BLACK)
    screen.blit(player1_label, (WIDTH // 2 - 50, 400))
    screen.blit(player2_label, (WIDTH // 2 - 50, 50))


def draw_stones():
    """Draw stones inside pits and stores."""
    for i, count in enumerate(stones):
        x, y = (PIT_POSITIONS + STORE_POSITIONS)[i]  # Center of the pit or store
        for j in range(count):
            # Arrange stones in a grid inside the pit or store
            dx = (j % 4 - 1.5) * (STONE_RADIUS * 2.5)  # Spread stones horizontally
            dy = (j // 4 - 0.5) * (STONE_RADIUS * 2.5)  # Spread stones vertically
            pygame.draw.circle(screen, STONE_COLOR, (x + int(dx), y + int(dy)), STONE_RADIUS)


def animate_stone_movement(start, end):
    """Animate a single stone moving between pits."""
    start_x, start_y = (PIT_POSITIONS + STORE_POSITIONS)[start]
    end_x, end_y = (PIT_POSITIONS + STORE_POSITIONS)[end]
    x, y = start_x, start_y

    for _ in range(30):  # Smooth transition
        x += (end_x - start_x) / 30
        y += (end_y - start_y) / 30
        screen.fill((34, 139, 34))
        draw_board()
        draw_stones()
        pygame.draw.circle(screen, HIGHLIGHT, (int(x), int(y)), STONE_RADIUS)
        pygame.display.flip()
        time.sleep(0.02)


def handle_click(pos):
    """Handle clicks on pits."""
    for i, pit_pos in enumerate(PIT_POSITIONS):
        dist = ((pit_pos[0] - pos[0]) ** 2 + (pit_pos[1] - pos[1]) ** 2) ** 0.5
        if dist <= PIT_RADIUS:
            return i
    return None


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked_pit = handle_click(event.pos)
            if clicked_pit is not None and stones[clicked_pit] > 0:
                # Move stones from clicked pit (for now, simply animate to next pit)
                stone_count = stones[clicked_pit]
                stones[clicked_pit] = 0
                for _ in range(stone_count):
                    next_pit = (clicked_pit + 1) % len(stones)
                    animate_stone_movement(clicked_pit, next_pit)
                    stones[next_pit] += 1
                    clicked_pit = next_pit

    # Redraw the board
    draw_board()
    draw_stones()
    pygame.display.flip()

pygame.quit()
sys.exit()
