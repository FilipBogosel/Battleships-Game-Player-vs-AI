import random

#custom exception classes
class InvalidShipPlacementError(Exception):
    pass

class InvalidShotError(Exception):
    pass

class Board:
    def __init__(self, size=7):
        self.size = size
        self.grid = [["~" for _ in range(size)] for _ in range(size)]
        self.ships = []

    def place_ship(self, ship):
        if not self.is_valid_position(ship.coordinates):
            raise InvalidShipPlacementError("Invalid position for ship placement.")
        for coord in ship.coordinates:
            x, y = coord
            self.grid[x][y] = "S"
        self.ships.append(ship)

    def is_valid_position(self, coordinates):
        for x, y in coordinates:
            if not (0 <= x < self.size and 0 <= y < self.size):
                return False
            if self.grid[x][y] != "~":
                return False
        return True

    def receive_shot(self, x, y):
        if not (0 <= x < self.size and 0 <= y < self.size):
            raise InvalidShotError("Shot is out of bounds.")
        if self.grid[x][y] == "S":
            self.grid[x][y] = "X"
            return True
        elif self.grid[x][y] == "~":
            self.grid[x][y] = "O"
        return False
    def all_ships_sunk(self):
        return all(self.grid[x][y] != "S" for ship in self.ships for x, y in ship.coordinates)

class Ship:
    def __init__(self, size, start, orientation):
        self.size = size
        self.coordinates = self.calculate_coordinates(start, orientation, size)

    @staticmethod
    def calculate_coordinates(start, orientation, size):
        x, y = start
        if orientation == "up":
            return [(x - i, y) for i in range(size)]
        elif orientation == "down":
            return [(x + i, y) for i in range(size)]
        elif orientation == "left":
            return [(x, y - i) for i in range(size)]
        elif orientation == "right":
            return [(x, y + i) for i in range(size)]

    def is_sunk(self, board):
        return all(board.grid[x][y] == "X" for x, y in self.coordinates)
