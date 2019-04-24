import re
import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
MAIN_URL = "https://scoresaber.com"

#userid:string -> all_songs:dict
def all_song_data(userid):
    player_page = requests.get(MAIN_URL + userid)
    srch_rslt = BeautifulSoup(player_page.text, "lxml")
    maxpage = int(srch_rslt.find_all("a", class_="pagination-link")[10].string)
    all_songs = {}
    for page in tqdm(range(1, maxpage+1)):
        songs = requests.get(MAIN_URL + userid + "&page={}&sort=1".format(page))
        srch_rslt = BeautifulSoup(songs.text, "lxml")
        for i in range(0, 8):
            if srch_rslt.find_all("span", class_="scoreTop ppWeightedValue")[0].text == "(0.00pp)":
                break
            else:
                song_data = srch_rslt.find_all("tbody")[0].find_all("tr")[i]#srch_rslt.find_all("tbody")[0].find_all("tr")[i].span.text
                songname = song_data.span.text
                song = {
                    "pp": float(song_data.find("span", class_="scoreTop ppValue").text),
                    "accuracy": song_data.find("span", class_="scoreBottom").text,
                    "img": song_data.img.get("src"),
                    "leaderboard": song_data.a.get("href"),
                    "rank": "#" + re.sub(r'\D', '', song_data.th.text)
                }
            all_songs[songname] = song
        else:
            continue
        break
    return all_songs

#page:int, line:int -> ranker_serch_result:bs4
def return_player_data(page, line):
    usr_rank_page_html = requests.get(MAIN_URL + "/global/{}".format(page))
    usr_rank_soup = BeautifulSoup(usr_rank_page_html.text, "lxml")
    ranking_list = usr_rank_soup.tbody.find_all("tr")
    return ranking_list[line]

#username:string -> userid:string, rank:int
def srch_usr_name(username):
    usr_srch_html = requests.get(MAIN_URL + "/global?search={}".format(username))
    srch_rslt = BeautifulSoup(usr_srch_html.text, "lxml")
    for i in range(0,10):
        name = srch_rslt.find_all("span", class_="songTop pp")[i].string
        if name == username:
            userid = srch_rslt.find_all("td", class_="player")[0].a.get("href")
            rank = int(re.sub(r'\D', '', srch_rslt.find_all("td", class_="rank")[i].string))
            print(userid)
            return userid, rank
        else:
            #error
            pass

#rank:int -> userid:string
def get_ranker(rank):
    page,line = divmod(rank, 50)
    if line == 0:
        player_data = return_player_data(page, 49)
    else:
        player_data = return_player_data(page+1, line-1)
    userid = player_data.find_all("td", class_="player")[0].a.get("href")
    return userid

#usr_songdata:dic, above_usr_songdata:dic -> pp_gap_list_sorted:list[dic]
def compare_song_pp(usr_songdata, above_usr_songdata):
    song_list = usr_songdata.keys()
    compare_result = []
    for song in tqdm(song_list):
        try:
            pp_gap = above_usr_songdata[song]["pp"] - usr_songdata[song]["pp"]
        except KeyError:
            pass
        else:
            ppgap_data = {
                "songname": song,
                "pp_gap": pp_gap,
            }
            compare_result.append(ppgap_data)
    pp_gap_list_sorted = sorted(compare_result, key=lambda x:x["pp_gap"], reverse=True)
    return pp_gap_list_sorted


