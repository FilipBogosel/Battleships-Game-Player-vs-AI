from Board.Board import InvalidShipPlacementError, InvalidShotError
from Game.Game import Game
import random
from texttable import Texttable
class UI:
    def __init__(self):
        self.game = Game()

    def display_board(self, board, hide_ships=False):
        table = Texttable()
        for row in board.grid:
            display_row = []
            for cell in row:
                if hide_ships and cell == "S":
                    display_row.append("~")
                else:
                    display_row.append(cell)
            table.add_row(display_row)
        print(table.draw())

    def get_human_ship_placement(self):
        ships = []
        print("Place your ships (size, x, y, orientation):")
        for size in [2, 2, 3, 3, 4]:
            while True:
                try:
                    x, y = map(int, input(f"Enter start position for ship of size {size}: ").split())
                    orientation = input("Enter orientation (up, down, left, right): ")
                    ships.append((size, (x, y), orientation))
                    break
                except InvalidShipPlacementError as e:
                    print(e)
        return ships

    def get_human_shot(self):
        while True:
            try:
                x, y = map(int, input("Enter your shot coordinates (x y): ").split())
                return x, y
            except InvalidShotError as e:
                print(e)

    def run(self):
        print("Welcome to Battleships!")
        while True:
            try:
                human_ships = self.get_human_ship_placement()
                self.game.setup_human_ships(human_ships)
                break
            except InvalidShipPlacementError as e:
                print(e)
                print("Invalid ship placement. Please try again.")

        self.game.setup_computer_ships()

        while not self.game.check_winner():
            if self.game.current_turn == "human":
                print("Your board:")
                self.display_board(self.game.human_board)
                print("Computer's board:")
                self.display_board(self.game.computer_board, hide_ships=True)

            if self.game.current_turn == "human":
                x, y = self.get_human_shot()
            else:
                print("Computer's turn...")
                if self.game.last_successful_shot_adiacents:
                    x, y = self.game.last_successful_shot_adiacents.pop()
                    # Check if the shot is valid (not already taken)
                    while not (0 <= x < 7 and 0 <= y < 7) or self.game.human_board.grid[x][y] in ["X", "O"]:
                        if not self.game.last_successful_shot_adiacents:
                            # If we run out of adjacent positions, generate random coordinates
                            x, y = random.randint(0, 6), random.randint(0, 6)
                            while self.game.human_board.grid[x][y] in ["X", "O"]:
                                x, y = random.randint(0, 6), random.randint(0, 6)
                            break
                        x, y = self.game.last_successful_shot_adiacents.pop()
                else:
                    # Initialize with random coordinates
                    x, y = random.randint(0, 6), random.randint(0, 6)
                    # Make sure we don't shoot at the same place twice
                    while self.game.human_board.grid[x][y] in ["X", "O"]:
                        x, y = random.randint(0, 6), random.randint(0, 6)
                print(f"Computer shoots at: {x}, {y}")

            self.game.take_turn(x, y)

        winner = self.game.check_winner()
        print(f"{winner.capitalize()} wins!")