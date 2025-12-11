from PyQt6.QtWidgets import QApplication, QMainWindow
from vote_gui import *
from vote_logic import *

def main():
    app = QApplication([])
    window = QMainWindow()
    ui = Ui_VoteWindow()
    ui.setupUi(window)
    logic = Logic(ui)

    window.show()
    app.exec()

if __name__ == "__main__":
    main()

