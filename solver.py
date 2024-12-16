import copy  # Pour créer des copies d'objets
import math  # Pour utiliser des valeurs comme inf
import time


class MancalaBoard:
    def __init__(self):
        self.board = {
            "A": 4,
            "B": 4,
            "C": 4,
            "D": 4,
            "E": 4,
            "F": 4,  # Fosses du joueur 1
            "G": 4,
            "H": 4,
            "I": 4,
            "J": 4,
            "K": 4,
            "L": 4,  # Fosses du joueur 2
            "1": 0,
            "2": 0,  # Magasins des joueurs, initialement vides
        }

        self.player1_pits = ("A", "B", "C", "D", "E", "F")
        self.player2_pits = ("G", "H", "I", "J", "K", "L")

        self.opposite_pits = {
            "A": "G",
            "B": "H",
            "C": "I",
            "D": "J",
            "E": "K",
            "F": "L",
            "G": "A",
            "H": "B",
            "I": "C",
            "J": "D",
            "K": "E",
            "L": "F",
        }

        self.next_pit = {
            "A": "B",
            "B": "C",
            "C": "D",
            "D": "E",
            "E": "F",
            "F": "1",
            "G": "2",
            "H": "G",
            "I": "H",
            "J": "I",
            "K": "J",
            "L": "K",
            "1": "L",
            "2": "A",
        }

    def possibleMoves(self, player):
        if player == 1:
            return [pit for pit in self.player1_pits if self.board[pit] > 0]
        elif player == 2:
            return [pit for pit in self.player2_pits if self.board[pit] > 0]
        return []


    def doMove(self, player, pit):
        seeds = self.board[pit]
        if seeds == 0:
            return False

        self.board[pit] = 0
        current_pit = pit

        while seeds > 0:
            current_pit = self.next_pit[current_pit]
            if current_pit == "1" and player == 2:
                continue
            if current_pit == "2" and player == 1:
                continue
            self.board[current_pit] += 1
            seeds -= 1

        if (
            current_pit in self.player1_pits
            and player == 1
            and self.board[current_pit] == 1
        ):
            opposite_pit = self.opposite_pits[current_pit]
            # if self.board[opposite_pit] > 0:
            self.board["1"] += self.board[current_pit] + self.board[opposite_pit]
            self.board[current_pit] = 0
            self.board[opposite_pit] = 0

        elif (
            current_pit in self.player2_pits
            and player == 2
            and self.board[current_pit] == 1
        ):
            opposite_pit = self.opposite_pits[current_pit]
            # if self.board[opposite_pit] > 0:
            self.board["2"] += self.board[current_pit] + self.board[opposite_pit]
            self.board[current_pit] = 0
            self.board[opposite_pit] = 0

        return True


class Game:
    def __init__(self, computer_side, human_side):
        self.state = MancalaBoard()
        # self.player_side = {"COMPUTER": "1", "HUMAN": "2"}
        self.player_side = {1: computer_side, -1: human_side}

    def gameOver(self, emit_func=None):
        if sum(self.state.board[pit] for pit in self.state.player1_pits) == 0:
            for pit in self.state.player2_pits:
                time.sleep(1)
                self.state.board["2"] += self.state.board[pit]
                self.state.board[pit] = 0
                if emit_func:
                    emit_func(
                        {
                            "board": self.state.board.copy(),
                            "current_pit": [pit, "2"],
                        }
                    )
            return True

        if sum(self.state.board[pit] for pit in self.state.player2_pits) == 0:
            for pit in self.state.player1_pits:
                time.sleep(1)
                self.state.board["1"] += self.state.board[pit]
                self.state.board[pit] = 0
                if emit_func:
                    emit_func(
                        {
                            "board": self.state.board.copy(),
                            "current_pit": [pit, "1"],
                        }
                    )
            return True

        return False

    def findWinner(self):
        score_player1 = self.state.board["1"]
        score_player2 = self.state.board["2"]

        if score_player1 > score_player2:
            return 1, score_player1  # Player 1 wins
        elif score_player2 > score_player1:
            return 2, score_player2  # Player 2 wins
        else:
            return 0, score_player1  # Draw

    def evaluate(self):
        return (
            self.state.board[str(self.player_side[1])]
            - self.state.board[str(self.player_side[-1])]
        )


def minimaxAlphaBetaPruning(game, player, depth, alpha, beta):
    if game.gameOver() or depth == 1:
        return game.evaluate(), None

    if player == 1:  # Maximizing for Computer
        best_value = -math.inf
        best_pit = None
        for pit in game.state.possibleMoves(game.player_side[player]):
            child_game = copy.deepcopy(game)
            child_game.state.doMove(game.player_side[player], pit)
            value, _ = minimaxAlphaBetaPruning(
                child_game, -player, depth - 1, alpha, beta
            )
            if value > best_value:
                best_value = value
                best_pit = pit
            if best_value >= beta:
                break
            if best_value > alpha:
                alpha = best_value
    else:  
        best_value = math.inf
        best_pit = None
        for pit in game.state.possibleMoves(game.player_side[player]):
            child_game = copy.deepcopy(game)
            child_game.state.doMove(game.player_side[player], pit)
            value, _ = minimaxAlphaBetaPruning(
                child_game, -player, depth - 1, alpha, beta
            )
            if value < best_value:
                best_value = value
                best_pit = pit
            if best_value <= alpha:
                break
            if best_value < beta:
                beta = best_value
    return best_value, best_pit


class Play:
    def __init__(self, human_side=1, computer_side=2, current_player=1):
        self.depth = 5
        self.current_player = current_player
        self.game = Game(computer_side, human_side)
        self.state = self.game.state
        self.playing = False

    def humanTurn(self):
        print("Your turn!")
        print("Current board:", self.game.state.board)
        moves = self.game.state.possibleMoves(self.game.player_side[-1])
        print(f"Available moves: {moves}")

        while True:
            move = input("Choose a pit: ").upper()
            if move in moves:
                self.game.state.doMove(self.game.player_side[-1], move)
                print("Current board:", self.game.state.board)
                break
            else:
                print("Invalid move. Try again.")

    def computerTurn(self):
        print("Computer's turn!")
        _, move = minimaxAlphaBetaPruning(self.game, 1, self.depth, -math.inf, math.inf)
        print(f"Computer chooses pit {move}")
        self.game.state.doMove(self.game.player_side[1], move)

    def play(self):
        while not self.game.gameOver():
            if self.current_player == self.game.player_side[-1]:
                self.humanTurn()
            else:
                self.computerTurn()

            self.current_player = 3 - self.current_player  # Toggle between 1 and 2

        winner, score = self.game.findWinner()
        if winner == 0:
            print("It's a draw!")
        else:
            print(f"Player {winner} wins with {score} seeds!")


def setupGame():
    print("Welcome to Mancala!")

    while True:
        choice = input("Choose your side (1 for Player 1, 2 for Player 2): ").strip()
        if choice in ("1", "2"):
            human_side = int(choice)
            computer_side = 3 - human_side
            break
        print("Invalid choice. Please select 1 or 2.")

    while True:
        first = input("Do you want to go first? (yes or no): ").strip().lower()
        if first in ("yes", "no"):
            current_player = human_side if first == "yes" else computer_side
            break
        print("Invalid choice. Please type 'yes' or 'no'.")

    return human_side, computer_side, current_player


def main():
    human_side, computer_side, current_player = setupGame()
    game = Play(
        human_side=human_side,
        computer_side=computer_side,
        current_player=current_player,
    )
    game.play()


if __name__ == "__main__":
    main()


