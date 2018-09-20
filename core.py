import requests
from bs4 import BeautifulSoup
import json
import time

with open('action.json') as f:
    jsondata = json.load(f)

start = time.time()
for data in jsondata["data"]:
    print(data["title"])
    page = requests.get("https://www.youtube.com/results?search_query=" + data["title"] + " trailer")
    soup = BeautifulSoup(page.content, 'html.parser')
    trailer_html = soup.find_all("h3", class_="yt-lockup-title")

    for a in trailer_html:
        trailer = a.find("a")["href"]
        if ("googleadservices" not in trailer):
            print(trailer)
            break

end = time.time()
print(end - start)
