import sys, getopt
import requests
import zipfile
import json
from io import BytesIO
URL_DETAIL="https://manga.bilibili.com/twirp/comic.v2.Comic/ComicDetail?device=pc&platform=web"
URL_IMAGE_INDEX="https://manga.bilibili.com/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web"
URL_MANGA_HOST="https://manga.hdslb.com"
URL_IMAGE_TOKEN="https://manga.bilibili.com/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web"

def download(url,filename):
    r=requests.get(url, stream=True)
    f=open(filename, "wb")
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
    f.close()

def getChapters(comic_id):
    data=requests.post(URL_DETAIL,data={"comic_id": comic_id}).json()["data"]
    print("[Info]", data["title"])
    print("[Info]", data["evaluate"])
    data["ep_list"].reverse()
    return data["ep_list"]

def decode(data,comic_id,ep_id):
    key=[ep_id&0xff,ep_id>>8&0xff,ep_id>>16&0xff,ep_id>>24&0xff,
        comic_id&0xff,comic_id>>8&0xff,comic_id>>16&0xff,comic_id>>24&0xff]
    for i in range(len(data)):
        data[i]^=key[i%8]
    file=BytesIO(data)
    zf=zipfile.ZipFile(file)
    data=json.loads(zf.read("index.dat"))
    zf.close()
    file.close()
    return data

def getImageIndex(comic_id,ep_id):
    data=requests.post(URL_IMAGE_INDEX,data={"ep_id": ep_id}).json()["data"]
    data=bytearray(requests.get(data["host"]+data["path"]).content[9:])
    return decode(data,comic_id,ep_id)

def getToken(url):
    data=requests.post(URL_IMAGE_TOKEN,data={"urls": "[\""+url+"\"]"}).json()["data"][0]
    return data["url"]+"?token="+data["token"]

def main():
    pass
