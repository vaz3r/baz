import requests
from bs4 import BeautifulSoup
import json
import time
import re

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def getTrailer(movie_title):
    try:
        page = requests.get("https://www.youtube.com/results?search_query=" + movie_title + " trailer")
        soup = BeautifulSoup(page.content, 'html.parser')
        trailer_html = soup.find_all("h3", class_="yt-lockup-title")

        trailer = ""

        if len(trailer_html) <= 0:
            #V2 JSON SCRAPING
            scripts = soup.find_all("script")

            for script in scripts:
                if 'window["ytInitialData"]' in script.text:
                    trailer = find_between(script.text, '"videoId":', '",').replace('"', "").strip()
                    trailer = "https://www.youtube.com/watch?v=" + trailer
                    break
        else:
            #V1 HTML SCRAPING
            for a in trailer_html:
                trailer = a.find("a")["href"]
                if ("googleadservices" not in trailer):
                    trailer = trailer.replace("/watch?v=", "https://www.youtube.com/watch?v=")
                    break
        
        return trailer
    except:
        print("Exception: getTrailer")
        return "null"

with open('action.json') as f:
    jsondata = json.load(f)

start = time.time()
for data in jsondata["data"]:
    print(getTrailer(data["title"]))
end = time.time()
print(end - start)