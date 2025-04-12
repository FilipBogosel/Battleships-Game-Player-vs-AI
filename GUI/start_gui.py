import sys
from PyQt5.QtWidgets import QApplication
from gui_game import BattleshipGameWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BattleshipGameWindow()
    window.show()
    sys.exit(app.exec_())