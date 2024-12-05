import pygame
import sys

class Colors:
    """Classe de constantes pour les couleurs du jeu"""
    BACKGROUND = (245, 222, 179)  # Blé
    BOARD = (139, 69, 19)  # Marron foncé
    PIT = (222, 184, 135)  # Marron clair
    STONE = (169, 169, 169)  # Gris
    TEXT = (0, 0, 0)  # Noir

class GameConfig:
    """Configuration du jeu Mancala"""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PITS_PER_PLAYER = 6
    INITIAL_STONES_PER_PIT = 4

class MancalaBoard:
    """Représentation logique du plateau de Mancala"""
    def __init__(self, config):
        self.config = config
        self.reset_board()
    
    def reset_board(self):
        """Réinitialise le plateau de jeu"""
        total_pits = self.config.PITS_PER_PLAYER * 2
        self.pits = [self.config.INITIAL_STONES_PER_PIT] * total_pits
        self.stores = [0, 0]  # Stores pour chaque joueur
        self.current_player = 0
    
    def move_stones(self, start_pit):
        """Logique de distribution des pierres"""
        stones = self.pits[start_pit]
        self.pits[start_pit] = 0
        current_pit = start_pit

        while stones > 0:
            current_pit = (current_pit + 1) % (self.config.PITS_PER_PLAYER * 2)
            
            # Sauter le store de l'adversaire
            if current_pit == (self.config.PITS_PER_PLAYER if self.current_player == 1 else self.config.PITS_PER_PLAYER * 2):
                continue
            
            self.pits[current_pit] += 1
            stones -= 1
        
        # Logique de capture
        self._handle_capture(current_pit)
        
        # Changement de joueur
        if current_pit not in [self.config.PITS_PER_PLAYER - 1, self.config.PITS_PER_PLAYER * 2 - 1]:
            self.current_player = 1 - self.current_player
    
    def _handle_capture(self, last_pit):
        """Gère la capture des pierres"""
        if (self.current_player == 0 and 
            self.config.PITS_PER_PLAYER <= last_pit < self.config.PITS_PER_PLAYER * 2 and 
            self.pits[last_pit] == 1):
            opposite_pit = len(self.pits) - 1 - last_pit
            if self.pits[opposite_pit] > 0:
                captured = self.pits[opposite_pit] + 1
                self.stores[self.current_player] += captured
                self.pits[last_pit] = 0
                self.pits[opposite_pit] = 0

class MancalaRenderer:
    """Rendu graphique du jeu Mancala"""
    def __init__(self, screen, board, config):
        self.screen = screen
        self.board = board
        self.config = config
        self.font = pygame.font.Font(None, 36)
    
    def draw_board(self):
        """Dessine l'ensemble du plateau de jeu"""
        self.screen.fill(Colors.BACKGROUND)
        self._draw_game_board()
        self._draw_pits()
        self._draw_stores()
        self._draw_player_turn()
    
    def _draw_game_board(self):
        """Dessine le plateau principal"""
        pygame.draw.rect(
            self.screen, 
            Colors.BOARD, 
            (100, 200, 600, 200), 
            0
        )
    
    def _draw_pits(self):
        """Dessine les pits pour chaque joueur"""
        pit_width, pit_height = 80, 120
        pit_spacing = 10
        
        # Pits du haut (Joueur 2)
        for i in range(self.config.PITS_PER_PLAYER):
            x = 200 + i * (pit_width + pit_spacing)
            pygame.draw.ellipse(
                self.screen, 
                Colors.PIT, 
                (x, 250, pit_width, pit_height)
            )
            self._render_pit_text(
                self.board.pits[i], 
                (x + pit_width//2, 310)
            )
        
        # Pits du bas (Joueur 1)
        for i in range(self.config.PITS_PER_PLAYER):
            x = 200 + i * (pit_width + pit_spacing)
            pygame.draw.ellipse(
                self.screen, 
                Colors.PIT, 
                (x, 350, pit_width, pit_height)
            )
            self._render_pit_text(
                self.board.pits[i + self.config.PITS_PER_PLAYER], 
                (x + pit_width//2, 410)
            )
    
    def _render_pit_text(self, stones, position):
        """Affiche le nombre de pierres dans un pit"""
        text = self.font.render(str(stones), True, Colors.TEXT)
        text_rect = text.get_rect(center=position)
        self.screen.blit(text, text_rect)
    
    def _draw_stores(self):
        """Dessine les stores des joueurs"""
        pygame.draw.rect(
            self.screen, 
            Colors.PIT, 
            (100, 250, 80, 200)
        )
        pygame.draw.rect(
            self.screen, 
            Colors.PIT, 
            (700, 250, 80, 200)
        )
        
        # Texte des stores
        store1_text = self.font.render(
            str(self.board.stores[0]), 
            True, 
            Colors.TEXT
        )
        store2_text = self.font.render(
            str(self.board.stores[1]), 
            True, 
            Colors.TEXT
        )
        
        self.screen.blit(
            store1_text, 
            store1_text.get_rect(center=(140, 350))
        )
        self.screen.blit(
            store2_text, 
            store2_text.get_rect(center=(740, 350))
        )
    
    def _draw_player_turn(self):
        """Affiche le tour du joueur actuel"""
        player_text = self.font.render(
            f"Tour du Joueur {self.board.current_player + 1}", 
            True, 
            Colors.TEXT
        )
        player_rect = player_text.get_rect(
            center=(self.config.SCREEN_WIDTH//2, 50)
        )
        self.screen.blit(player_text, player_rect)

class MancalaGame:
    """Classe principale gérant le jeu Mancala"""
    def __init__(self):
        pygame.init()
        self.config = GameConfig()
        self.screen = pygame.display.set_mode(
            (self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Jeu Mancala")
        
        self.board = MancalaBoard(self.config)
        self.renderer = MancalaRenderer(self.screen, self.board, self.config)
    
    def _get_clicked_pit(self, pos):
        """Détermine le pit cliqué par le joueur"""
        pit_width, pit_height = 80, 120
        pit_spacing = 10
        start_x = 200
        
        for i in range(self.config.PITS_PER_PLAYER):
            x = start_x + i * (pit_width + pit_spacing)
            pit_index = i + (self.config.PITS_PER_PLAYER if self.board.current_player == 0 else 0)
            
            # Vérification de la zone de clic
            if (x < pos[0] < x + pit_width and 
                (350 if self.board.current_player == 0 else 250) < pos[1] < 
                (350 if self.board.current_player == 0 else 250) + pit_height):
                
                if self.board.pits[pit_index] > 0:
                    return pit_index
        return None
    
    def run(self):
        """Boucle principale du jeu"""
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        clicked_pit = self._get_clicked_pit(event.pos)
                        if clicked_pit is not None:
                            self.board.move_stones(clicked_pit)
            
            self.renderer.draw_board()
            pygame.display.flip()
            clock.tick(30)

def main():
    """Point d'entrée du jeu"""
    game = MancalaGame()
    game.run()

if __name__ == "__main__":
    main()
    
    
