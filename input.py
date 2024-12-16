import pygame
import sys

def get_user_char(board):
    pygame.init()
    screen = pygame.display.set_mode((1000, 400))
    pygame.display.set_caption("Button Selection")
    font = pygame.font.Font(None, 36)
    
    # Define buttons
    button_width = 60
    button_height = 40
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
                        
    pygame.quit()
    return selected_char

def main(board):
    char = get_user_char(board)
    while char == "":
        char = get_user_char(board)   
    return char