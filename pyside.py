import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import ScoreSaber

songs = [{"song":"songname", "pp": "123", "image":"kivy.png", "accuracy": "50%", "rank": "43", "ppgap": "+11"},
             {"song":"songname2", "pp": "32", "image":"kivy.png", "accuracy": "50%", "rank": "43", "ppgap": "+11"},
             {"song":"songname3", "pp": "54", "image":"kivy.png", "accuracy": "50%", "rank": "43", "ppgap": "+11"}]

#widgetsの設定
class CustomQWidget(QWidget):
    def __init__ (self, parent = None):
        super(CustomQWidget, self).__init__(parent)
        #レイアウト作成
        self.textQVBoxLayout = QHBoxLayout() #song layout
        self.usersppQLabel   = QLabel() #
        self.ppgapQLabel     = QLabel() 
        self.accuracyQLabel  = QLabel() #
        self.rankQLabel      = QLabel()
        #レイアウトへwidget追加
        self.textQVBoxLayout.addWidget(self.usersppQLabel)
        self.textQVBoxLayout.addWidget(self.accuracyQLabel)
        
        #レイアウト作成
        self.songQVBoxLayout = QVBoxLayout()
        self.songQLabel      = QLabel()
        #追加
        self.songQVBoxLayout.addWidget(self.songQLabel)
        self.songQVBoxLayout.addLayout(self.textQVBoxLayout)
        #レイアウト作成
        self.allQHBoxLayout  = QHBoxLayout()
        self.iconQLabel      = QLabel()
        #レイアウトへicon widget追加
        self.allQHBoxLayout.addWidget(self.rankQLabel, 0)
        self.allQHBoxLayout.addWidget(self.iconQLabel, 1)
        self.allQHBoxLayout.addLayout(self.songQVBoxLayout, 2)
        self.allQHBoxLayout.addWidget(self.ppgapQLabel, 3)
        #レイアウトの設定
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        """
        self.songQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.usersppQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')
"""
    def setSong (self, text):
        self.songQLabel.setText(text)

    def setPP (self, text):
        self.usersppQLabel.setText(text)

    def setPPgap(self, text):
        self.ppgapQLabel.setText(text)

    def setAccuracy(self, text):
        self.accuracyQLabel.setText(text)

    def setRank(self, text):
        self.rankQLabel.setText(text)
    
    def setIcon (self, imagePath):
        #画像を追加、リサイズ
        image = QPixmap(imagePath)
        resized = image.scaled(64, 64)
        self.iconQLabel.setPixmap(resized)

class ButtonWidgets(QWidget):
    """docstring for ButtonWidgets"""
    def __init__(self, parent = None):
        super(ButtonWidgets, self).__init__()
        self.MainWindowLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        #make list widget
        self.myQListWidget = QListWidget(self)

        for song in songs:
            song_name = song["song"]
            pp = song["pp"] + "pp"
            img = song["image"]
            ppgap = song["ppgap"]
            accuracy = "accuracy: {}%".format(song["accuracy"])
            rank = "#" + song["rank"]

            myQCustomQWidget = CustomQWidget()
            myQCustomQWidget.setSong(song_name)
            myQCustomQWidget.setPP(pp)
            myQCustomQWidget.setIcon(img)
            myQCustomQWidget.setPPgap(ppgap)
            myQCustomQWidget.setAccuracy(accuracy)
            myQCustomQWidget.setRank(rank)

            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        
        #button set
        refButton = QPushButton("ref")
        usernameBox = QLineEdit()

        self.myQListWidget.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.myQListWidget.setFrameStyle(QFrame.NoFrame)
        
        #add widget
        self.buttonLayout.addWidget(refButton)
        self.buttonLayout.addWidget(usernameBox)

        #set layout and wedgets -> main layout
        self.MainWindowLayout.addWidget(self.myQListWidget)
        self.MainWindowLayout.addLayout(self.buttonLayout)
        # set layout
        self.setLayout(self.MainWindowLayout)

#main window
class AppMainWindow(QMainWindow):
    def __init__ (self):
        super(AppMainWindow, self).__init__()
        #window setting
        self.setMinimumHeight(500)
        self.setMinimumWidth(700)
        self.setMaximumHeight(500)
        self.setMaximumWidth(700)

        windowItems = ButtonWidgets()
        self.setCentralWidget(windowItems)
app = QApplication(sys.argv)
window = AppMainWindow()
window.show()
app.exec_()



