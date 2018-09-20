import sys
import os
import json

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