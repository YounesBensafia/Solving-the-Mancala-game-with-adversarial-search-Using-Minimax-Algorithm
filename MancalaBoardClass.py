
# ----- DONE
# from an import a
class MancalaBoard:
    
    # The game is represented as a board, which can be modeled using a dictionary. 
    # The keys represent
    # the indices of the 12 pits and 2 stores, and the values represent the number of seeds in each. The
    # pits of Player 1 are labeled with letters from A to F, and the pits of Player 2 are labeled with letters
    # from G to L. The stores for players 1 and 2 are represented by corresponding numbers
    
    def __init__(self):
        self.board = {
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4, #PLAYER1
            
            1: 0, #STORE 1
            
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4, # PLAYER2
            
            2: 0  #STORE 2
        }
        
        
        self.player_pits = {
            1: ('A', 'B', 'C', 'D', 'E', 'F'),  # Pits player 1
            2: ('G', 'H', 'I', 'J', 'K', 'L')   # Pits player 2
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
        # 1. The first {player} selects a {pit} on their side of the board and collects all the seeds from it;
        
        seeds = self.board[pit] # HENA RAHO IL SELECTS
        self.board[pit] = 0 # COLLECTS THE SEEDS FROM IT
        current_pit = pit
        
        # 2. Moving counterclockwise, the player drops one seed into each pit until they have no more seeds in hand
        while seeds > 0:
            # print(current_pit)
            current_pit = self.next_pit[current_pit]
            # 2. The  player  can  place  a  seed  in  any  pit  on  the  board  (including  their  own  store),  except  in  the opponent's store
            if (player == 1 and current_pit == 2) or (player == 2 and current_pit == 1):
                continue
            self.board[current_pit] += 1
            seeds -= 1
 
        
        if current_pit in self.player_pits[player] and self.board[current_pit] == 1:
            # 3. If the last seed placed lands in an empty pit on the player's side, that seed and all the seeds in the 
            # opposite pit (belonging to the opponent) go to the player and are placed in their store; 
            opposite_pit = self.opposite_pits[current_pit]
            # if current_pit in self.player_pits[player]:
            self.board[player] = self.board[player] + self.board[opposite_pit] + 1
            self.board[current_pit] = 0
            self.board[opposite_pit] = 0
        # a(self.board)
