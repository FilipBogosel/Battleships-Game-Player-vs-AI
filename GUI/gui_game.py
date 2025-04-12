from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QMessageBox)
from PyQt5.QtCore import QTimer
from game_board import GameBoardWidget
from ship_placement import ShipPlacementDialog
from Game.Game import Game

class BattleshipGameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Battleships Game")
        self.setMinimumSize(800, 600)
        
        self.game = Game()
        self.init_ui()
        self.start_new_game()
        
    def init_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Game title
        title = QLabel("🚢 Naval Clash: Python Battleship")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # Game boards layout
        boards_layout = QHBoxLayout()
        
        # Human board
        human_layout = QVBoxLayout()
        human_label = QLabel("Your Board")
        human_layout.addWidget(human_label)
        
        self.human_board_widget = GameBoardWidget(interactive=False)
        human_layout.addWidget(self.human_board_widget)
        
        boards_layout.addLayout(human_layout)
        
        # Computer board
        computer_layout = QVBoxLayout()
        computer_label = QLabel("Computer's Board")
        computer_layout.addWidget(computer_label)
        
        self.computer_board_widget = GameBoardWidget()
        self.computer_board_widget.cell_clicked.connect(self.on_computer_board_clicked)
        computer_layout.addWidget(self.computer_board_widget)
        
        boards_layout.addLayout(computer_layout)
        
        main_layout.addLayout(boards_layout)
        
        # Game status
        self.status_label = QLabel("Welcome to Battleships!")
        self.status_label.setStyleSheet("font-size: 16px; margin: 10px;")
        main_layout.addWidget(self.status_label)
        
        # Control buttons
        buttons_layout = QHBoxLayout()
        
        new_game_button = QPushButton("New Game")
        new_game_button.clicked.connect(self.start_new_game)
        buttons_layout.addWidget(new_game_button)
        
        main_layout.addLayout(buttons_layout)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def start_new_game(self):
        self.game = Game()
        
        # Open ship placement dialog
        placement_dialog = ShipPlacementDialog(self)
        if placement_dialog.exec_():
            ship_data = placement_dialog.get_ship_data()
            self.game.setup_human_ships(ship_data)
            self.game.setup_computer_ships()
            
            # Update the boards
            self.update_boards()
            self.status_label.setText("Game started! Your turn.")
        
    def update_boards(self):
        self.human_board_widget.update_from_board(self.game.human_board)
        self.computer_board_widget.update_from_board(self.game.computer_board, hide_ships=True)
        
    def on_computer_board_clicked(self, x, y):
        if self.game.current_turn == "human":
            self.status_label.setText(f"You fired at ({x}, {y})...")
            
            # Process human turn
            try:
                hit = self.game.computer_board.receive_shot(x, y)
                if hit:
                    self.status_label.setText(f"Hit! You hit a ship at ({x}, {y})!")
                else:
                    self.status_label.setText(f"Miss! Your shot at ({x}, {y}) hit water.")
                
                self.game.current_turn = "computer"
                self.update_boards()
                
                # Check for winner
                winner = self.game.check_winner()
                if winner:
                    self.game_over(winner)
                    return
                
                # Computer's turn after a short delay
                QTimer.singleShot(1000, self.computer_turn)
                
            except Exception as e:
                self.status_label.setText(f"Invalid shot: {str(e)}")
                
    def computer_turn(self):
        self.status_label.setText("Computer is thinking...")
        
        # Get computer's shot
        if self.game.last_successful_shot_adiacents:
            x, y = self.game.last_successful_shot_adiacents.pop()
            # Check if the shot is valid
            while not (0 <= x < 7 and 0 <= y < 7) or self.game.human_board.grid[x][y] in ["X", "O"]:
                if not self.game.last_successful_shot_adiacents:
                    x, y = self.get_random_shot()
                    break
                x, y = self.game.last_successful_shot_adiacents.pop()
        else:
            x, y = self.get_random_shot()
            
        # Process computer's turn
        hit = self.game.human_board.receive_shot(x, y)
        
        # Update AI strategy if hit
        if hit:
            self.status_label.setText(f"Computer hit your ship at ({x}, {y})!")
            self.game.last_successful_shot = (x, y)
            self.game.last_successful_shot_adiacents = self.game.get_adiacent_positions(x, y)
        else:
            self.status_label.setText(f"Computer missed at ({x}, {y}).")
            
        self.game.current_turn = "human"
        self.update_boards()
        
        # Check for winner
        winner = self.game.check_winner()
        if winner:
            self.game_over(winner)
            
    def get_random_shot(self):
        """Get a random valid shot for the computer"""
        import random
        x, y = random.randint(0, 6), random.randint(0, 6)
        while self.game.human_board.grid[x][y] in ["X", "O"]:
            x, y = random.randint(0, 6), random.randint(0, 6)
        return x, y
        
    def game_over(self, winner):
        """Handle game over state"""
        message = f"Game Over! {winner.capitalize()} wins!"
        self.status_label.setText(message)
        
        # Show all ships
        self.computer_board_widget.update_from_board(self.game.computer_board, hide_ships=False)
        
        # Show game over dialog
        QMessageBox.information(self, "Game Over", message)