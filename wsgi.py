from flask import Flask
import requests
from bs4 import BeautifulSoup
import json

application = Flask(__name__)

@application.route("/")
def hello():
    return "Hello World!"

@application.route("/gotrailers")
def hello():
    with open('action.json') as f:
    jsondata = json.load(f)

    bigdata = ""

    for data in jsondata["data"]:
        print(data["title"])
        page = requests.get("https://www.youtube.com/results?search_query=" + data["title"] + " trailer")
        soup = BeautifulSoup(page.content, 'html.parser')
        trailer_html = soup.find("h3", class_="yt-lockup-title")
        trailer = trailer_html.find("a")["href"]
        print(trailer)

        bigdata += data["title"] + " = " + trailer

    with open("data.txt", 'w') as f:
        f.write(bigdata)
    
    return "Done!"

if __name__ == "__main__":
    application.run()
