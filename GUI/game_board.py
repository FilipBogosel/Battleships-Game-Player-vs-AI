from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

class GameBoardWidget(QWidget):
    cell_clicked = pyqtSignal(int, int)
    
    def __init__(self, board_size=7, interactive=True, parent=None):
        super().__init__(parent)
        self.board_size = board_size
        self.interactive = interactive
        self.buttons = []
        self.init_ui()
        
    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(2)
        
        # Create grid of buttons
        for row in range(self.board_size):
            button_row = []
            for col in range(self.board_size):
                button = QPushButton()
                button.setFixedSize(40, 40)
                button.setFont(QFont('Arial', 12))
                if self.interactive:
                    button.clicked.connect(lambda _, r=row, c=col: self.cell_clicked.emit(r, c))
                layout.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)
            
        self.setLayout(layout)
        
    def update_cell(self, row, col, state):
        """
        Update the cell appearance based on its state
        States: '~' (water), 'S' (ship), 'X' (hit), 'O' (miss)
        """
        button = self.buttons[row][col]
        
        if state == '~':
            button.setStyleSheet("background-color: #ADD8E6;")  # Light blue for water
            button.setText("")
        elif state == 'S':
            button.setStyleSheet("background-color: #808080;")  # Gray for ship
            button.setText("")
        elif state == 'X':
            button.setStyleSheet("background-color: #FF0000;")  # Red for hit
            button.setText("X")
        elif state == 'O':
            button.setStyleSheet("background-color: #FFFFFF;")  # White for miss
            button.setText("O")
            
    def update_from_board(self, board, hide_ships=False):
        """Update the entire board from a Board object"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                cell_state = board.grid[row][col]
                if hide_ships and cell_state == 'S':
                    cell_state = '~'
                self.update_cell(row, col, cell_state)
                
    def highlight_ship_placement(self, coordinates, valid=True):
        """Highlight cells for ship placement preview"""
        # Reset all cells first
        for row in self.buttons:
            for button in row:
                button.setStyleSheet("background-color: #ADD8E6;")  # Reset to water
                
        # Highlight the ship cells
        color = "#90EE90" if valid else "#FFA07A"  # Light green if valid, light red if invalid
        for x, y in coordinates:
            if 0 <= x < self.board_size and 0 <= y < self.board_size:
                self.buttons[x][y].setStyleSheet(f"background-color: {color};")