#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask,render_template,request,session

#Flaskオブジェクトの生成
app = Flask(__name__)

from apiclient.discovery import build
from apiclient.errors import HttpError
import cgi
import cgitb
import os.path
import html

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/result",methods=["post"])
def test():
    key = request.form["key"]
    category = request.form["category"]
    maxNumber = int(request.form["maxNumber"])

    DEVELOPER_KEY = 'AIzaSyDxpI6IrA6jitzr6LFvqhhjmp8AnMNXQTY'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    youtube = build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY
    )

    search_response = youtube.search().list(q=key,part='id,snippet',maxResults = maxNumber,order=category).execute()

    array = []
    
    for sr in search_response.get("items", []):

        title = sr['snippet']['title']
        channelName = sr['snippet']['channelTitle']
        published = sr['snippet']['publishedAt']
        published = published[0:10]
        channelTitle = sr['snippet']['channelTitle']
        if sr["id"]["kind"] == "youtube#video":
            url = "https://www.youtube.com/embed/" + sr['id']['videoId']
        elif sr["id"]["kind"] == "youtube#channel":
            url = "https://www.youtube.com/enbed/" + sr["id"]["channelId"]
        else:
            url = "https://www.youtube.com/embed/" + sr["id"]["playlistId"]

        array.append(title)
        array.append(channelTitle)
        array.append(published)
        array.append(url)
    
    return render_template("result.html",array=array)

    
#おまじない
if __name__ == "__main__":
    app.run(debug=True)
