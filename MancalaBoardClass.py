
# ----- DONE
# from an import a
class MancalaBoard:
    
    def __init__(self):
        self.board = {
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4, #PLAYER1
            
                                1: 0, #STORE 1
            
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4, # PLAYER2
            
                                2: 0  #STORE 2
        }
        
        
        self.player_pits = {
            1: ('A', 'B', 'C', 'D', 'E', 'F'),  
            2: ('G', 'H', 'I', 'J', 'K', 'L') 
        }
                
    
        self.opposite_pits = { 
            'A': 'G', 'B': 'H', 'C': 'I', 'D': 'J', 'E': 'K', 'F': 'L',
            'G': 'A', 'H': 'B', 'I': 'C', 'J': 'D', 'K': 'E', 'L': 'F'
        }
        
        self.next_pit = {
            'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F':1, 1:'L', 
            'L':'K', 'K':'J', 'J':'I', 'I':'H', 'H':'G', 'G':2, 2:'A'
        }
        
    def possibleMoves(self, player):
        """ returns the possible moves (i.e., the indices of the pits belonging to the player that contain seeds) """
        if player == 1:
            return [pit for pit in self.player_pits[1] if self.board[pit] > 0]
        elif player == 2:
            return [pit for pit in self.player_pits[2] if self.board[pit] > 0]
        else:
            return []

    def doMove(self, player, pit):
        
        seeds = self.board[pit]
        self.board[pit] = 0 
        current_pit = pit
        
        while seeds > 0:
            current_pit = self.next_pit[current_pit]
            if (player == 1 and current_pit == 2) or (player == 2 and current_pit == 1):
                continue
            self.board[current_pit] += 1
            seeds -= 1
 
        
        if current_pit in self.player_pits[player] and self.board[current_pit] == 1:
            opposite_pit = self.opposite_pits[current_pit]
            self.board[player] = self.board[player] + self.board[opposite_pit] + 1
            self.board[current_pit] = 0
            self.board[opposite_pit] = 0
            
