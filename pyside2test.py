import tempfile
import requests
import shutil
import os
#tempファイル生成 /imports/images/songs/94732B3C04674601C131430DD2B28C7E.png
cwd = os.getcwd()
img_tmpdir = tempfile.mkdtemp(dir=cwd)

img_id = "/imports/images/songs/94732B3C04674601C131430DD2B28C7E.png"

def dl_imgfile(dir, url, songname):
    url = "https://scoresaber.com" + url
    img = requests.get(url, stream=True)
    path = dir + "/" + songname + ".png"
    with open(path, 'wb') as f:
            f.write(img.content)
    return path


di = dl_imgfile(img_tmpdir, img_id, "M2U - Quo Vadis Expert+")
print(di)
#tempファイル削除
shutil.rmtree(img_tmpdir)
