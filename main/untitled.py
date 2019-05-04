import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class AppMainWindow(QMainWindow):
    def __init__ (self):
        super(AppMainWindow, self).__init__()
        refButton = QPushButton("")
        refButton.setIcon(QIcon(QPixmap("assets/button_ref.png")))
        refButton.setStyleSheet("QPushButton{border: 0px solid; height: 21px;width: 71px;}")
        refButton.setIconSize(QSize(71, 21))
        self.setCentralWidget(refButton)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    app.exec_()

