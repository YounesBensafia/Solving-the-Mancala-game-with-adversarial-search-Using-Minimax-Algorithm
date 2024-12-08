class GameClass:
    def __init__(self, state, playerSide):
        """
        Args:
            state (an instance of the MancalaBoard class): represent the game state.
            playerSide (dictionary):  stores the player side chosen by the human and
            the computer (player1 or player2).
        """
        self.state = state
        self.playerSide = playerSide

    def gameOver(self):
        """The function gameOver(), which checks if the game has ended (i.e., all the pits of one player are 
        empty). This function will also collect all remaining seeds in the opponent s pits and place them 
        in their store"""
        
        player1_empty = all(self.state.board[pit] == 0 for pit in self.state.player_pits[1])
        player2_empty = all(self.state.board[pit] == 0 for pit in self.state.player_pits[2])
        
        if player1_empty or player2_empty:
            if player1_empty:
                for pit in self.state.player_pits[2]:
                    self.state.board[2] += self.state.board[pit]
                    self.state.board[pit] = 0
            elif player2_empty:
                for pit in self.state.player_pits[1]:
                    self.state.board[1] += self.state.board[pit]
                    self.state.board[pit] = 0
            return True 
        return False

    def findWinner(self):
        player1_score = self.state.board[1]
        player2_score = self.state.board[2]
        if player1_score > player2_score:
            return 'HUMAN', player1_score
        elif player2_score > player1_score:
            return 'COMPUTER', player2_score
        else:
            return 'draw', player1_score

    def getChildren(self):
        children = []
        for pit in self.state.player_pits[self.playerSide]:
            if self.state.board[pit] > 0:
                new_state = self.state.copy()
                new_state.state.doMove(self.playerSide, pit)
                next_player = 1 if self.playerSide == 2 else 2
                children.append(GameClass(new_state, next_player))
        return children
    def h(self):
        computer_store = self.state.board[self.playerSide['COMPUTER']]
        human_store = self.state.board[self.playerSide['HUMAN']]
        return computer_store - human_store
    

    def evaluate(node):
        # to do


