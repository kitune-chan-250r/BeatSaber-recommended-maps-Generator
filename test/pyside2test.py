#退避
    def ref_button(self):
        username = self.usernameBox.text()
        self.myQListWidget.clear()
        self.usernameBox.setText(username + " push")
        #userid,rank = ScoreSaber.srch_usr_name(username)
        global songs
        #songs = ScoreSaber.all_song_data(userid)
        
        my_userid,my_rank = ScoreSaber.srch_usr_name(username)
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

            myQListWidgetItem = QListWidgetItem(self.myQListWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        
        self.myQListWidget.update()