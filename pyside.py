import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import ScoreSaber
import requests



songs = [{"song":"songname", "pp": "123", "image":"kivy.png", "accuracy": "50%", "rank": "43", "ppgap": "+11"},
             {"song":"songname2", "pp": "32", "image":"kivy.png", "accuracy": "50%", "rank": "43", "ppgap": "+11"},
             {"song":"songname3", "pp": "54", "image":"kivy.png", "accuracy": "50%", "rank": "43", "ppgap": "+11"}]

def dl_imgfile(url):
    url = "https://scoresaber.com" + url
    img = requests.get(url, stream=True)
    return img.content

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
        #image = QPixmap(imagePath)
        qimage = QPixmap()
        qimage.loadFromData(imagePath)
        resized = qimage.scaled(50, 50)
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
            ppgap = song["ppgap"]
            accuracy = "accuracy: {}%".format(song["accuracy"])
            rank = "#" + song["rank"]
            #make image
            #img = "./assets/ki - vy.png"

            myQCustomQWidget = CustomQWidget()
            myQCustomQWidget.setSong(song_name)
            myQCustomQWidget.setPP(pp)
            #myQCustomQWidget.setIcon(img)
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
        refButton = QPushButton("ref", self)
        refButton.clicked.connect(self.ref_button)
        self.usernameBox = QLineEdit()

        self.myQListWidget.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.myQListWidget.setFrameStyle(QFrame.NoFrame)
        
        #add widget
        self.buttonLayout.addWidget(refButton)
        self.buttonLayout.addWidget(self.usernameBox)

        #set layout and wedgets -> main layout
        self.MainWindowLayout.addWidget(self.myQListWidget)
        self.MainWindowLayout.addLayout(self.buttonLayout)
        # set layout
        self.setLayout(self.MainWindowLayout)

    def ref_button(self):
        username = self.usernameBox.text()
        self.bgp = BuckGroundProcess()
        self.bgp.addItem_QList.connect(self.addItem_refresh)
        self.bgp.setup(username)
        self.bgp.start()

    def addItem_refresh(self, widget_item):
        self.myQListWidget.addItem(widget_item)

#qthread class
class BuckGroundProcess(QThread):
    addItem_QList = Signal( str ) #listにアイテムを渡す
    setItem_Qlist = Signal()
    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        self.username = ""

    def setup(self, username):
        self.username = username

    def run(self): #バックグラウンド処理
        #userid,rank = ScoreSaber.srch_usr_name(username)
        bw = ButtonWidgets()
        global songs
        #songs = ScoreSaber.all_song_data(userid)
        print(self.username)
        my_userid,my_rank = ScoreSaber.srch_usr_name(self.username)
        aboveusr_id = ScoreSaber.get_ranker(my_rank-1)

        my_songdata = ScoreSaber.all_song_data(my_userid)
        aboveusr_songdata = ScoreSaber.all_song_data(aboveusr_id)

        pp_gap = ScoreSaber.compare_song_pp(my_songdata, aboveusr_songdata)
        
        songs = pp_gap[0:5]
        #songs.append({"song":"songname4", "pp": "154", "image":"kivy.png", "accuracy": "50%", "rank": "1", "ppgap": "+11"})
        #refresh list
        for song in songs:
            song_name = song["songname"]
            ppgap = str(song["pp_gap"])
            tmp = ScoreSaber.srch_song_data(song_name, my_songdata)

            pp = str(tmp["pp"]) + "pp"

            img = dl_imgfile(tmp["img"])
            print(img)
            accuracy = tmp["accuracy"]
            rank = str(tmp["rank"])

            myQCustomQWidget = CustomQWidget()
            myQCustomQWidget.setSong(song_name)
            myQCustomQWidget.setPP(pp)
            myQCustomQWidget.setIcon(img)
            myQCustomQWidget.setPPgap(ppgap)
            myQCustomQWidget.setAccuracy(accuracy)
            myQCustomQWidget.setRank(rank)

            myQListWidgetItem = QListWidgetItem(bw.myQListWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            #bw.myQListWidget.addItem(myQListWidgetItem)
            self.signal_WidgetItem(myQListWidgetItem)
            bw.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        
        bw.myQListWidget.update()
        self.finished.emit()
    def signal_WidgetItem(self,widget_item):#ユーザー定義シグナル(addItem_QList)を呼ぶ
        self.addItem_QList.emit(widget_item)
    def signal_CustomWidget(self, Custom_widget):
        self.setItem_Qlist.emit(CustomQWidget)

#main window
class AppMainWindow(QMainWindow):
    def __init__ (self):
        super(AppMainWindow, self).__init__()
        #window setting
        self.setMinimumHeight(540)
        self.setMinimumWidth(780)
        self.setMaximumHeight(540)
        self.setMaximumWidth(780)

        windowItems = ButtonWidgets()
        self.setCentralWidget(windowItems)

    def closeEvent(self, event):
        #アプリ終了時に呼ばれる
        event.accept()

app = QApplication(sys.argv)
window = AppMainWindow()
window.show()
app.exec_()



