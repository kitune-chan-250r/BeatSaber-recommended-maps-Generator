import requests
import json

def get_songdata():
    return requests.get("http://scoresaber.com/api.php?function=get-leaderboards&cat=1&page=1&limit=20").json()

###func###

print(get_songdata())