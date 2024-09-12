from PyQt5.QtWidgets import QApplication
from UI_main import App
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = App()
    app.exec_()

