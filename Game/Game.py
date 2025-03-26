from Board.Board import Board, Ship, InvalidShipPlacementError, InvalidShotError
import random


class Game:
    def __init__(self):
        self.human_board = Board()
        self.computer_board = Board()
        self.current_turn = "human"
        self.last_successful_shot = None
        self.last_successful_shot_adiacents = []

    def setup_computer_ships(self):
        for size in [2, 2, 3, 3, 4]:
            placed = False
            while not placed:
                x, y = random.randint(0, 6), random.randint(0, 6)
                orientation = random.choice(["up", "down", "left", "right"])
                ship = Ship(size, (x, y), orientation)
                if self.computer_board.is_valid_position(ship.coordinates):
                    self.computer_board.place_ship(ship)
                    placed = True

    def setup_human_ships(self, ship_data):
        for size, start, orientation in ship_data:
            ship = Ship(size, start, orientation)
            if self.human_board.is_valid_position(ship.coordinates):
                self.human_board.place_ship(ship)
            else:
                raise InvalidShipPlacementError("Invalid position for ship placement.")

    def take_turn(self, x, y):
        board = self.computer_board if self.current_turn == "human" else self.human_board
        hit = board.receive_shot(x, y)
        if hit and self.current_turn == "computer":
            # Add computer strategy to aim better next shot
            self.last_successful_shot = (x, y)
            self.last_successful_shot_adiacents = self.get_adiacent_positions(x, y)

        self.current_turn = "computer" if self.current_turn == "human" else "human"

    def get_adiacent_positions(self, x, y):
        return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    def check_winner(self):
        if self.human_board.all_ships_sunk():
            return "computer"
        elif self.computer_board.all_ships_sunk():
            return "human"
        return None