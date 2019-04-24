import ScoreSaber
from kivy.uix.recycleview import RecycleView
from kivy.app import App

my_userid,my_rank = ScoreSaber.srch_usr_name("fox100")
aboveusr_id = ScoreSaber.get_ranker(my_rank-1)

my_songdata = ScoreSaber.all_song_data(my_userid)
aboveusr_songdata = ScoreSaber.all_song_data(aboveusr_id)

pp_gap = ScoreSaber.compare_song_pp(my_songdata, aboveusr_songdata)

for i in range(0,5):
    print(pp_gap[i])

