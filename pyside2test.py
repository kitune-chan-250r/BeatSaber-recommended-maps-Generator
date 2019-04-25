
from PySide2.QtWidgets import *

class MyLayoutDialog(QDialog):
    def __init__(self, parent=None):
        super(MyLayoutDialog, self).__init__(parent)
        self.setWindowTitle("My Layout Dialog")
        
        # 並べるボタンを作成
        buttonA = QPushButton("Button A")
        buttonB = QPushButton("Button B")
        buttonC = QPushButton("Button C")
        
        # 水平方向にボタンを並べる
        layout = QHBoxLayout()
        layout.addWidget(buttonA)
        layout.addWidget(buttonB)
        layout.addWidget(buttonC)
        self.setLayout(layout)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = MyLayoutDialog()
    ui.show()
    app.exec_()