import requests
import json
from bs4 import BeautifulSoup
from yt_dlp.YoutubeDL import YoutubeDL
import sys



# ydl = YoutubeDL(params={'format':'[height<=1080]'})
ydl = None
params = {}
for i in range(len(sys.argv)):
    if sys.argv[i]=="-f":
        frm = sys.argv[i+1]
        # print(frm)
        params['format'] = frm

ydl = YoutubeDL(params=params)





def get_latest_info(channelHandle):
    respose = requests.get(f"https://www.youtube.com/@{channelHandle}/videos")
    soup = BeautifulSoup(respose.text,"html.parser")
    targetstr = '"url":"/watch?v='
    soup = str(soup)
    stindex = soup.index(targetstr)
    stvideoid = soup[stindex+len(targetstr):stindex+len(targetstr)+11]
    return stvideoid

def download_latest_video(channelHandle):
    videoid = get_latest_info(channelHandle)
    # downloadedvids = open(f"downloadedVideos_{channelHandle}.txt","r")
    downloadedvids = {}

    try:
        vidfile_read = open("downloadedVideos.json","r")
        downloadedvids = json.load(vidfile_read)
        vidfile_read.close()
    except json.decoder.JSONDecodeError:
        pass
    except FileNotFoundError:
        vidfile_read = open("downloadedVideos.json","w")
        vidfile_read.close()
    if (channelHandle in downloadedvids):
        if downloadedvids[channelHandle] != videoid:
            vidfile_write = open("downloadedVideos.json","w")
            ydl.download([f"https://www.youtube.com/watch?v={videoid}"])
            downloadedvids[channelHandle]=videoid
            json.dump(downloadedvids,vidfile_write,indent=4)
            vidfile_write.close()
        else:
            print(f"No new {channelHandle} videos to download.")
    else:
            vidfile_write = open(f"downloadedVideos.json","w")
            ydl.download([f"https://www.youtube.com/watch?v={videoid}"])
            downloadedvids[channelHandle]=videoid
            json.dump(downloadedvids,vidfile_write,indent=4)
            vidfile_write.close()

    # else:
    #     print(f"No new {channelHandle} videos to download")





if __name__=="__main__":
    download_latest_video(sys.argv[-1])

    

