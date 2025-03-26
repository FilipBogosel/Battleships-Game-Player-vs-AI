import unittest
from Board import Board, Ship, InvalidShipPlacementError, InvalidShotError

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_place_ship_valid(self):
        ship = Ship(3, (2, 2), "right")
        self.board.place_ship(ship)
        self.assertEqual(self.board.grid[2][2], "S")
        self.assertEqual(self.board.grid[2][3], "S")
        self.assertEqual(self.board.grid[2][4], "S")

    def test_place_ship_invalid(self):
        ship = Ship(3, (6, 6), "right")
        with self.assertRaises(InvalidShipPlacementError):
            self.board.place_ship(ship)

    def test_is_valid_position(self):
        ship = Ship(3, (2, 2), "right")
        self.assertTrue(self.board.is_valid_position(ship.coordinates))
        invalid_ship = Ship(3, (6, 6), "right")
        self.assertFalse(self.board.is_valid_position(invalid_ship.coordinates))

    def test_receive_shot_hit(self):
        ship = Ship(3, (2, 2), "right")
        self.board.place_ship(ship)
        self.assertTrue(self.board.receive_shot(2, 2))
        self.assertEqual(self.board.grid[2][2], "X")

    def test_receive_shot_miss(self):
        self.assertFalse(self.board.receive_shot(0, 0))
        self.assertEqual(self.board.grid[0][0], "O")

    def test_all_ships_sunk(self):
        ship = Ship(2, (2, 2), "right")
        self.board.place_ship(ship)
        self.board.receive_shot(2, 2)
        self.board.receive_shot(2, 3)
        self.assertTrue(self.board.all_ships_sunk())

class TestShip(unittest.TestCase):

    def test_calculate_coordinates_up(self):
        ship = Ship(3, (3, 3), "up")
        self.assertEqual(ship.coordinates, [(3, 3), (2, 3), (1, 3)])

    def test_calculate_coordinates_down(self):
        ship = Ship(3, (3, 3), "down")
        self.assertEqual(ship.coordinates, [(3, 3), (4, 3), (5, 3)])

    def test_calculate_coordinates_left(self):
        ship = Ship(3, (3, 3), "left")
        self.assertEqual(ship.coordinates, [(3, 3), (3, 2), (3, 1)])

    def test_calculate_coordinates_right(self):
        ship = Ship(3, (3, 3), "right")
        self.assertEqual(ship.coordinates, [(3, 3), (3, 4), (3, 5)])

if __name__ == '__main__':
    unittest.main()