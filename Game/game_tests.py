import unittest
from Game import Game
from Board.Board import Board, Ship, InvalidShipPlacementError, InvalidShotError

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_setup_computer_ships(self):
        self.game.setup_computer_ships()
        ship_count = sum(cell == "S" for row in self.game.computer_board.grid for cell in row)
        self.assertEqual(ship_count, 14)  # Assuming the total ship size is 14

    def test_setup_human_ships(self):
        human_ships = [(2, (0, 0), "right"), (3, (1, 0), "down")]
        self.game.setup_human_ships(human_ships)
        self.assertEqual(self.game.human_board.grid[0][0], "S")
        self.assertEqual(self.game.human_board.grid[0][1], "S")
        self.assertEqual(self.game.human_board.grid[1][0], "S")
        self.assertEqual(self.game.human_board.grid[2][0], "S")
        self.assertEqual(self.game.human_board.grid[3][0], "S")

    def test_take_turn(self):
        self.game.setup_computer_ships()
        self.game.setup_human_ships([(2, (0, 0), "right")])
        self.game.take_turn(0, 0)
        self.game.take_turn(0, 0)
        self.assertEqual(self.game.human_board.grid[0][0], "X")
        self.game.take_turn(1, 1)
        self.game.take_turn(1, 1)
        self.assertEqual(self.game.human_board.grid[1][1], "O")

    def test_get_adjacent_positions(self):
        adj_cells = self.game.get_adiacent_positions(3, 3)
        expected_cells = [(2, 3), (4, 3), (3, 2), (3, 4)]
        self.assertEqual(set(adj_cells), set(expected_cells))


    def test_check_winner(self):
        self.game.setup_human_ships([(2, (0, 0), "right")])
        self.game.setup_computer_ships()
        self.game.human_board.receive_shot(0, 0)
        self.game.human_board.receive_shot(0, 1)
        self.assertEqual(self.game.check_winner(), "computer")

if __name__ == '__main__':
    unittest.main()