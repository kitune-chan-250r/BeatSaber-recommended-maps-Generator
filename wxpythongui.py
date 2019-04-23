# coding:utf-8
#pythonw {filename}
import wx
import re
import json
import requests
from bs4 import BeautifulSoup

from functools import wraps
import time
from tqdm import tqdm
def stop_watch(func) :
    @wraps(func)
    def wrapper(*args, **kargs) :
        start = time.time()
        result = func(*args,**kargs)
        process_time =  time.time() - start
        print(f"{func.__name__}は{process_time}秒かかりました")
        return result
    return wrapper

MAIN_URL = "https://scoresaber.com"
usrname = "fox100"

def all_song_data(usrid, maxpage):#usrid:string maxpage:int
    #request_url = MAIN_URL + usrid + "&page={}&sort=1".format(1)
    all_songs = {}
    for page in tqdm(range(1, maxpage+1)):
        songs = requests.get(MAIN_URL + usrid + "&page={}&sort=1".format(page))
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
            
    """
    songs = requests.get(MAIN_URL + usrid + "&page={}&sort=1".format(1))
    srch_rslt = BeautifulSoup(songs.text, "lxml")
    song = re.sub(r'\D', '',(srch_rslt.find_all("span", class_="scoreTop ppWeightedValue")[0].text))#
    print(int(song))
"""
#ランクを受けて一つ上の人のusridとmaxpageを返す
def ranker_above(rank):#retrun id,maxpage
    page,line = divmod(rank-1, 50)
    usr_rank_page_html = requests.get(MAIN_URL + "/global/{}".format(page+1))
    usr_rank_soup = BeautifulSoup(usr_rank_page_html.text, "html.parser")
    ranking_list = usr_rank_soup.tbody.find_all("tr")[line-1]
    usrid = ranking_list.find_all("td", class_="player")[0].a.get("href")
    player_page = requests.get(MAIN_URL + usrid)
    srch_rslt = BeautifulSoup(player_page.text, "lxml")#"html.parser"
    pagemax = srch_rslt.find_all("a", class_="pagination-link")[10].string
    
    return usrid, int(pagemax)
    
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
    return compare_result


    

def main():
    usr_srch_html = requests.get(MAIN_URL + "/global?search={}".format(usrname)) #検索 SirChartonson
    srch_rslt = BeautifulSoup(usr_srch_html.text, "lxml")# "lxml"


    for i in range(0,10):
        name = srch_rslt.find_all("span", class_="songTop pp")[i].string
        if name == usrname:
            usr_url = srch_rslt.find_all("td", class_="player")[0].a.get("href")
            rank = re.sub(r'\D', '', srch_rslt.find_all("td", class_="rank")[i].string)
            print(usr_url)
            break
        else:
            #完全一致無しの場合エラー
            pass

    player_page = requests.get(MAIN_URL + usr_url)
    srch_rslt = BeautifulSoup(player_page.text, "lxml")#"html.parser"
    pagemax = srch_rslt.find_all("a", class_="pagination-link")[10].string
    usr_songdata = all_song_data(usr_url, int(pagemax))

    aboveusr,above_pagemax = ranker_above(int(rank))
    above_usr_songdata = all_song_data(aboveusr, above_pagemax)

    pp_gap_list = compare_song_pp(usr_songdata, above_usr_songdata)
    pp_gap_list_sorted = sorted(pp_gap_list, key=lambda x:x["pp_gap"], reverse=True)
    return pp_gap_list_sorted
    """
    for i in range(0,10):
        print(pp_gap_list_sorted[i])
"""
#main()

def click_button_event(event):
	gaplist = main()
	for songs in range(0,10):
	    listbox.Append(gaplist[songs]["songname"]+"\n"+"gap = {}".format(gaplist[songs]["pp_gap"]))
	event.Skip()

app = wx.App()
main_frame = wx.Frame(None, wx.ID_ANY, u"課題曲生成機", size=(540, 280))
menu_panel = wx.Panel(main_frame, wx.ID_ANY, pos=(0, 0), size=(540,30))
menu_panel.SetBackgroundColour('#FF0000')
panel = wx.Panel(main_frame, wx.ID_ANY, pos=(0, 20), size=(540,250))
menu_panel.SetBackgroundColour('#000000')

listbox = wx.ListBox(panel, wx.ID_ANY, size=(540, 10), choices=[], style=wx.LB_SINGLE)
refresh_button = wx.Button(menu_panel, wx.ID_ANY, '更新')
main_frame.Bind(wx.EVT_BUTTON, click_button_event, refresh_button)

"""
gaplist = main()
for songs in range(0,10):
    listbox.Append(gaplist[songs]["songname"]+"\n"+"gap = {}".format(gaplist[songs]["pp_gap"]))
"""

menu_layout = wx.BoxSizer(wx.VERTICAL)
menu_layout.Add(refresh_button, 0, wx.GROW)
menu_layout.Add(menu_panel, 1, wx.EXPAND)
menu_layout.Add(panel, 1, wx.EXPAND)

layout = wx.BoxSizer(wx.VERTICAL)

layout.Add(listbox, 2, wx.EXPAND, 0)

panel.SetSizer(layout)

main_frame.SetSizer(menu_layout)
main_frame.Show()
app.MainLoop()






