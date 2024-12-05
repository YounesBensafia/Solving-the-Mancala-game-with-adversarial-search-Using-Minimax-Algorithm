class MancalaBoard:
    
    # The game is represented as a board, which can be modeled using a dictionary. 
    # The keys represent
    # the indices of the 12 pits and 2 stores, and the values represent the number of seeds in each. The
    # pits of Player 1 are labeled with letters from A to F, and the pits of Player 2 are labeled with letters
    # from G to L. The stores for players 1 and 2 are represented by corresponding numbers
    
    def __init__(self):
        self.board = {
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4, 1: 0,
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4, 2: 0
        }
        
        
        self.player1_pits = ('A', 'B', 'C', 'D', 'E', 'F')
        self.player2_pits = ('G', 'H', 'I', 'J', 'K', 'L')
        
        self.opposite_pits = { 
            'A': 'G', 'B': 'H', 'C': 'I', 'D': 'J', 'E': 'K', 'F': 'L',
            'G': 'A', 'H': 'B', 'I': 'C', 'J': 'D', 'K': 'E', 'L': 'F'
        }
        self.next_pit = {
            'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F'
        }
        
    def possibleMoves(self, player):
        """ returns the possible moves (i.e., the indices of the pits belonging to the player that contain seeds) """
        if player == 1:
            return [pit for pit in self.player1_pits if self.board[pit] > 0]
        elif player == 2:
            return [pit for pit in self.player2_pits if self.board[pit] > 0]
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

        if current_pit in self.player1_pits + self.player2_pits and self.board[current_pit] == 1:
            opposite_pit = self.opposite_pits[current_pit]
            if player == 1 and current_pit in self.player1_pits:
                self.board[1] += self.board[opposite_pit] + 1
                self.board[current_pit] = 0
                self.board[opposite_pit] = 0
            elif player == 2 and current_pit in self.player2_pits:
                self.board[2] += self.board[opposite_pit] + 1
                self.board[current_pit] = 0
                self.board[opposite_pit] = 0

        return current_pit
