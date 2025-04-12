from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QComboBox, QGroupBox)
from PyQt5.QtCore import Qt
from game_board import GameBoardWidget
from Board.Board import Ship, Board

class ShipPlacementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Place Your Ships")
        self.setMinimumSize(600, 500)
        
        self.board = Board()
        self.ships_to_place = [2, 2, 3, 3, 4]  # Ship sizes to place
        self.current_ship_index = 0
        self.current_position = (3, 3)  # Start in the middle
        self.current_orientation = "right"
        
        self.init_ui()
        self.update_ship_preview()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel("Place your ships on the board")
        instructions.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(instructions)
        
        # Game board
        self.board_widget = GameBoardWidget(interactive=False)
        main_layout.addWidget(self.board_widget)
        
        # Controls group
        controls_group = QGroupBox("Ship Controls")
        controls_layout = QVBoxLayout()
        
        # Ship info
        self.ship_info = QLabel()
        controls_layout.addWidget(self.ship_info)
        
        # Movement controls
        movement_layout = QHBoxLayout()
        
        self.up_button = QPushButton("↑")
        self.up_button.clicked.connect(lambda: self.move_ship("up"))
        
        self.down_button = QPushButton("↓")
        self.down_button.clicked.connect(lambda: self.move_ship("down"))
        
        self.left_button = QPushButton("←")
        self.left_button.clicked.connect(lambda: self.move_ship("left"))
        
        self.right_button = QPushButton("→")
        self.right_button.clicked.connect(lambda: self.move_ship("right"))
        
        movement_layout.addWidget(self.up_button)
        movement_layout.addWidget(self.down_button)
        movement_layout.addWidget(self.left_button)
        movement_layout.addWidget(self.right_button)
        
        controls_layout.addLayout(movement_layout)
        
        # Orientation control
        orientation_layout = QHBoxLayout()
        orientation_label = QLabel("Orientation:")
        self.orientation_combo = QComboBox()
        self.orientation_combo.addItems(["up", "down", "left", "right"])
        self.orientation_combo.setCurrentText("right")
        self.orientation_combo.currentTextChanged.connect(self.change_orientation)
        
        orientation_layout.addWidget(orientation_label)
        orientation_layout.addWidget(self.orientation_combo)
        
        controls_layout.addLayout(orientation_layout)
        
        # Place button
        self.place_button = QPushButton("Place Ship")
        self.place_button.clicked.connect(self.place_current_ship)
        controls_layout.addWidget(self.place_button)
        
        controls_group.setLayout(controls_layout)
        main_layout.addWidget(controls_group)
        
        self.setLayout(main_layout)
        
    def update_ship_info(self):
        if self.current_ship_index < len(self.ships_to_place):
            size = self.ships_to_place[self.current_ship_index]
            self.ship_info.setText(f"Placing ship {self.current_ship_index + 1} of {len(self.ships_to_place)} (Size: {size})")
        else:
            self.ship_info.setText("All ships placed!")
            
    def get_current_ship_coordinates(self):
        size = self.ships_to_place[self.current_ship_index]
        ship = Ship(size, self.current_position, self.current_orientation)
        return ship.coordinates
        
    def update_ship_preview(self):
        self.update_ship_info()
        
        if self.current_ship_index < len(self.ships_to_place):
            coordinates = self.get_current_ship_coordinates()
            valid = self.board.is_valid_position(coordinates)
            self.board_widget.update_from_board(self.board)
            self.board_widget.highlight_ship_placement(coordinates, valid)
            self.place_button.setEnabled(valid)
        else:
            self.accept()  # Close dialog when all ships are placed
            
    def move_ship(self, direction):
        x, y = self.current_position
        
        if direction == "up":
            x = max(0, x - 1)
        elif direction == "down":
            x = min(6, x + 1)
        elif direction == "left":
            y = max(0, y - 1)
        elif direction == "right":
            y = min(6, y + 1)
            
        self.current_position = (x, y)
        self.update_ship_preview()
        
    def change_orientation(self, orientation):
        self.current_orientation = orientation
        self.update_ship_preview()
        
    def place_current_ship(self):
        if self.current_ship_index < len(self.ships_to_place):
            size = self.ships_to_place[self.current_ship_index]
            ship = Ship(size, self.current_position, self.current_orientation)
            
            if self.board.is_valid_position(ship.coordinates):
                self.board.place_ship(ship)
                self.current_ship_index += 1
                
                if self.current_ship_index < len(self.ships_to_place):
                    # Reset position for next ship
                    self.current_position = (3, 3)
                    self.update_ship_preview()
                else:
                    # All ships placed
                    self.board_widget.update_from_board(self.board)
                    self.update_ship_info()
                    self.place_button.setEnabled(False)
                    # Auto-close after a short delay
                    self.accept()
                    
    def get_ship_data(self):
        """Return the ship data in the format expected by Game.setup_human_ships"""
        ship_data = []
        for ship in self.board.ships:
            # Extract the first coordinate (start position) and orientation
            start = ship.coordinates[0]
            
            # Determine orientation based on coordinates
            if len(ship.coordinates) > 1:
                x1, y1 = ship.coordinates[0]
                x2, y2 = ship.coordinates[1]
                
                if x2 < x1:
                    orientation = "up"
                elif x2 > x1:
                    orientation = "down"
                elif y2 < y1:
                    orientation = "left"
                else:
                    orientation = "right"
            else:
                orientation = "right"  # Default for size 1 ships
                
            ship_data.append((ship.size, start, orientation))
            
        return ship_data