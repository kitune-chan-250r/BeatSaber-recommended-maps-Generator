import sys
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import ScoreSaber
import requests
from multiprocessing import Pipe,Process


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
        self.song_font = QFont()
        self.song_font.setPointSize(20)

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
        self.songQLabel.setFont(self.song_font)
        self.songQLabel.setStyleSheet("QLabel{color: white}")

    def setPP (self, text):
        self.usersppQLabel.setText(text)
        self.usersppQLabel.setStyleSheet("QLabel{color: white}")

    def setPPgap(self, text):
        self.ppgapQLabel.setText(text)
        self.ppgapQLabel.setStyleSheet("QLabel{color: white}")

    def setAccuracy(self, text):
        self.accuracyQLabel.setText(text)
        self.accuracyQLabel.setStyleSheet("QLabel{color: white}")

    def setRank(self, text):
        self.rankQLabel.setText(text)
        self.rankQLabel.setStyleSheet("QLabel{color: white}")
    
    def setIcon (self, imagePath):
        #画像を追加、リサイズ
        #image = QPixmap(imagePath)
        qimage = QPixmap()
        qimage.loadFromData(imagePath)
        resized = qimage.scaled(50, 50)
        self.iconQLabel.setPixmap(resized)


class BuckGroundProcess(QThread):
    """listに入れるデータたち"""
    finSignal = Signal(dict)
    """"""

    def __init__(self,parent=None):
        QThread.__init__(self,parent)
        self.username = ""

    def setup(self, username):
        self.username = username

    def run(self): #バックグラウンド処理
        global songs

        print(self.username)
        """
        my_userid,my_rank = ScoreSaber.srch_usr_name(self.username)
        aboveusr_id = ScoreSaber.get_ranker(my_rank-1)

        my_songdata = ScoreSaber.all_song_data(my_userid)
        aboveusr_songdata = ScoreSaber.all_song_data(aboveusr_id)

        pp_gap = ScoreSaber.compare_song_pp(my_songdata, aboveusr_songdata)
        """
        main_to_sub,sub_to_main = Pipe() #通信用パイプ生成
        my_userid,my_rank = ScoreSaber.srch_usr_name(self.username)
        aboveusr_id = ScoreSaber.get_ranker(my_rank-1)

        def sub_proc(abov_id,pipe):#サブプロセス化する関数
            aboveusr_songdata = ScoreSaber.all_song_data(abov_id)
            pipe.send(aboveusr_songdata)
            return True
        pr = Process(target=sub_proc, args=(aboveusr_id, sub_to_main))
        pr.start()
        my_songdata = ScoreSaber.all_song_data(my_userid)
        aboveusr_songdata = main_to_sub.recv()
        pr.join()

        pp_gap = ScoreSaber.compare_song_pp(my_songdata, aboveusr_songdata)
        
        songs = pp_gap[0:5]
        print("send finsignal")
        self.finSignal.emit(my_songdata)
        
class ButtonWidgets(QWidget):
    thread = BuckGroundProcess()
    """docstring for ButtonWidgets"""
    def __init__(self, parent = None):
        super(ButtonWidgets, self).__init__()
        self.thread.finSignal.connect(self.updateQList)

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
            #img = "./assets/ki - vy.png QLineEdit { background-color: yellow }""

            myQCustomQWidget = CustomQWidget()
            myQCustomQWidget.setSong(song_name)
            myQCustomQWidget.setPP(pp)
            #myQCustomQWidget.setIcon(img)
            myQCustomQWidget.setPPgap(ppgap)
            myQCustomQWidget.setAccuracy(accuracy)
            myQCustomQWidget.setRank(rank)

            self.myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            # Set size hint
            self.myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.myQListWidget.addItem(self.myQListWidgetItem.setFlags(Qt.NoItemFlags))
            self.myQListWidget.setItemWidget(self.myQListWidgetItem, myQCustomQWidget)
        
        #button setting
        refButton = QPushButton("")
        refButton.setStyleSheet("QPushButton{height: 21px;width: 71px; border: 0px solid}")
        refButton.setIcon(QIcon(QPixmap("assets/button_ref.png")))
        refButton.setIconSize(QSize(71, 21))
        #x,y,w,h
        refButton.clicked.connect(self.ref_button)

        #status label setting
        self.status_label = QLabel()
        self.update_status("status")#init

        #QLine Edit setting
        self.usernameBox = QLineEdit()
        self.usernameBox.setMaximumWidth(160)

        self.usernameBox.setStyleSheet("QLineEdit{background-color: #2E2F29 ;color : white; border: none;height: 21px;width: 40px;}")
        self.myQListWidget.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.myQListWidget.setFrameStyle(QFrame.NoFrame)
        
        #add widget
        self.buttonLayout.addWidget(self.status_label)
        self.buttonLayout.addSpacing(400)
        self.buttonLayout.addWidget(self.usernameBox)
        self.buttonLayout.addWidget(refButton)

        #set layout and wedgets -> main layout
        self.MainWindowLayout.addWidget(self.myQListWidget)
        self.MainWindowLayout.addLayout(self.buttonLayout)
        # set layout
        self.setLayout(self.MainWindowLayout)

        #set stylesheet
        self.setStyleSheet("""QListWidget{background-color:#1E2125}""")

    def ref_button(self):
        self.update_status("Downloading song data...")
        self.myQListWidget.clear()
        username = self.usernameBox.text()
        #self.bgp = BuckGroundProcess()
        self.thread.setup(username)
        self.thread.start()

    def updateQList(self, my_songdata):
        my_songdata = my_songdata
        print("rcv finsignal")
        for song in songs:
            song_name = song["songname"]
            ppgap = str(round(song["pp_gap"], 2))
            tmp = ScoreSaber.srch_song_data(song_name, my_songdata)

            pp = str(tmp["pp"]) + "pp"

            img = dl_imgfile(tmp["img"])
            accuracy = tmp["accuracy"]
            rank = str(tmp["rank"])

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
            self.myQListWidget.addItem(myQListWidgetItem.setFlags(Qt.NoItemFlags))
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.myQListWidget.update()
        self.update_status("Analysis finished!")

    def update_status(self, status):
        self.status_label.setText(status)
        self.status_label.setStyleSheet("QLabel{color: white}")

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
        self.setStyleSheet("QMainWindow{background-color:#1E2125}")

    def closeEvent(self, event):
        #アプリ終了時に呼ばれる
        event.accept()

#main process
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    app.exec_()



