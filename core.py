import requests
from bs4 import BeautifulSoup
import json
from time import sleep
from b2blaze import B2
import time

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

def getYoutubeTrailer(movie_title):
    try:
        response = requests.get("https://www.googleapis.com/youtube/v3/search?q=" + movie_title + "%20trailer&maxResults=1&part=snippet&key=AIzaSyAuMfYQp9ClNz8ugf3DKmtSHOxa6P64QtM")
        jsonfile = json.loads(response.text)
        trailer = "https://www.youtube.com/watch?v=" + jsonfile["items"][0]["id"]["videoId"]
        return trailer
    except:
        print("Exception.")
        return "null"

start = time.time()

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
    
print("Ranking Databases...")

for genre in genres:
    f = open("popular\\" + genre + ".json","r")
    json_data = f.read()
    f.close()

    def sort_by_rating(data):
        try:
            return float(data['rating'])
        except:
            return 0

    data = json.loads(json_data)
    sorted_obj = dict(data) 
    sorted_obj['data'] = sorted(data['data'], key=sort_by_rating, reverse=True)

    final_data = json.dumps(sorted_obj)

    with open("best\\best-" + genre + ".json", 'w') as f:
        f.write(final_data)

    print(genre + " -> DONE.")

print("Uploading to server...")

b2 = B2(key_id="b41a85681294", application_key="001705ef3076ce3e3899d3a384fdef978e113e0d33")
bucket = b2.buckets.get('movies-db')

for genre in genres:
    #POPULAR DIR
    file_name = "popular\\" + genre + ".json"
    file_handle = open(file_name, 'rb')
    file_name_up = genre + ".json"
    file_upload = bucket.files.upload(contents=file_handle, file_name=file_name_up)
    #BEST DIR
    file_name = "best\\best-" + genre + ".json"
    file_name_up = "best-" + genre + ".json"
    file_handle = open(file_name, 'rb')
    file_upload = bucket.files.upload(contents=file_handle, file_name=file_name_up)

end = time.time()
time_taken = end - start

print("DONE.")
print("TIME TAKEN: " + str(time_taken))
