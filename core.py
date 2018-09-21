import requests
from bs4 import BeautifulSoup
import json
from time import sleep

genres = [
    'action',
    'drama',
    'adventure',
    'comedy',
    'animation',
    'sci_fi',
    'crime',
    'fantasy',
    'documentary',
    'family',
    'film_noir',
    'history',
    'horror',
    'musical',
    'mystery',
    'romance',
    'sport',
    'thriller',
    'war',
    'western',
    'biography'
]

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

def getYoutubeTrailer(movie_title):
    try:
        response = requests.get("https://www.googleapis.com/youtube/v3/search?q=" + movie_title + "%20trailer&maxResults=1&part=snippet&key=AIzaSyAuMfYQp9ClNz8ugf3DKmtSHOxa6P64QtM")
        jsonfile = json.loads(response.text)
        trailer = "https://www.youtube.com/watch?v=" + jsonfile["items"][0]["id"]["videoId"]
        return trailer
    except:
        print("Exception.")
        return "null"

for genre in genres:
    json_data = ""
    for i in range(1, 3):
        page = requests.get("https://www.imdb.com/search/title?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=b9121fa8-b7bb-4a3e-8887-aab822e0b5a7&pf_rd_r=6NPC34XD6M64C8QAYG53&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=moviemeter&genres=" + genre + "&explore=title_type,genres&title_type=movie&page=" + str(i))
        soup = BeautifulSoup(page.content, 'html.parser')

        itemsHTML = soup.find_all("div", class_="lister-item mode-advanced")

        for itemHTML in itemsHTML:
            data = {}
            movie_genre = itemHTML.find("span", class_="genre").text
            
            if ("animation" not in genre):
                if "Animation" in movie_genre:
                    continue

            popularityIndex = itemHTML.find("span", class_="lister-item-index unbold text-primary").text.replace(".", "")
            print(popularityIndex)

            year = itemHTML.find("span", class_="lister-item-year text-muted unbold").text

            linkTitle = itemHTML.find("h3", class_="lister-item-header").find("a",recursive=False)
            title = linkTitle.text + " " + year
            link = linkTitle['href']
            print(title)
            print(link)
            
            try:
                runtime = itemHTML.find("span", class_="runtime").text
            except:
                runtime = "N/A"
            
            print(runtime)

            try:
                rating = itemHTML.find("div", class_="inline-block ratings-imdb-rating")["data-value"]
            except:
                rating = "N/A"
            print(rating)

            summary = itemHTML.find_all("p", class_="text-muted")[1].text.strip()
            print(summary)

            image = itemHTML.find("img", class_="loadlate")['loadlate']
            vIndex = image.find("_V1")
            image = image[0:vIndex] + "_V1_UY600_CR0,0,0,600_AL_.jpg"
            print(image)

            # trailer = getTrailer(title)
            trailer = getYoutubeTrailer(title)
            print(trailer)
            print("=============================")
            data['popularityIndex'] = popularityIndex
            data['title'] = title
            data['link'] = link
            data['runtime'] = runtime
            data['rating'] = rating
            data['summary'] = summary
            data['image'] = image
            data['trailer'] = trailer

            json_object = json.dumps(data)
            json_data = json_data + json_object + ","

    json_data = json_data[:-1]

    file_name = "popular\\" + genre + ".json"

    with open(file_name, 'w') as f:
        f.write('{ "data": [' + json_data + ']}')
    
    print("Sleeping | Current Genre: " + genre)
    sleep(5)
    
