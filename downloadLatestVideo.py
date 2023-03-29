import requests
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
    downloadedvids = ""

    try:
        vidfile = open(f"downloadedVideos_{channelHandle}.txt","r")
        downloadedvids=vidfile.read()
        vidfile.close()
    except FileNotFoundError:
        vidfile = open(f"downloadedVideos_{channelHandle}.txt","w")
        vidfile.close()
    if (downloadedvids != videoid):
        vidfile = open(f"downloadedVideos_{channelHandle}.txt","w")
        vidfile.write(videoid)
        vidfile.close()
        ydl.download([f"https://www.youtube.com/watch?v={videoid}"])
    else:
        print(f"No new videos {channelHandle} to download")





if __name__=="__main__":
    # print(sys.argv[-1])
    # print(get_latest_info("druvrathee"))
    download_latest_video(sys.argv[-1])

    # with open("downloadedVideos_dhruvrathee.txt","r") as fl:
    #     print(fl.read()=="hello")
    #     print(fl.read()=="hello")
    #     # temp = fl.read()
    #     # print(temp)
    #     if(fl.read()=="hello"):
    #         print("ran")
    

