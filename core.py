import requests
from bs4 import BeautifulSoup
import json

with open('action.json') as f:
    jsondata = json.load(f)

for data in jsondata["data"]:
    print(data["title"])
    page = requests.get("https://www.youtube.com/results?search_query=" + data["title"] + " trailer")
    soup = BeautifulSoup(page.content, 'html.parser')
    trailer_html = soup.find("h3", class_="yt-lockup-title")
    trailer = trailer_html.find("a")["href"]
    print(trailer)
