import requests
from bs4 import BeautifulSoup
from yt_dlp.YoutubeDL import YoutubeDL
import json
import sys

"""
This python script is isolated script which uses yt-dlp to download latest videos of your latest
videos of your favorite youtuber. It uses channel handle to download latest videos and remembers which 
latest video was downloaded. If you run this script twice for same channel and no new video was uploaded
then it will download the first time and show no new video second time. Use this in following ways:

python3 downloadLatestVideos.py -f 'any format codes or specifiers' channel_handle_without_@


"""

ydl = None
params = {}
for i in range(len(sys.argv)):
    if sys.argv[i]=="-f":
        frm = sys.argv[i+1]
        params['format'] = frm

ydl = YoutubeDL(params=params)

# gives id of latest video of given channel handle
def get_latest_info(channelHandle):
    respose = requests.get(f"https://www.youtube.com/@{channelHandle}/videos")
    soup = BeautifulSoup(respose.text,"html.parser")
    targetstr = '"url":"/watch?v='
    soup = str(soup)
    stindex = soup.index(targetstr)
    stvideoid = soup[stindex+len(targetstr):stindex+len(targetstr)+11]
    return stvideoid

# downloads video only once for every channel handle
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


if __name__=="__main__":
    download_latest_video(sys.argv[-1])

    

