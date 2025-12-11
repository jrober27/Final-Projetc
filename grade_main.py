from PyQt6.QtWidgets import QApplication, QMainWindow
from grade_gui import *
from grade_logic import *

def main():
    app = QApplication([])
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    controller = GradeController(ui)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
