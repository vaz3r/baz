import sys
import os
import datetime

genres = [
    'Action',
    'Drama',
    'Adventure',
    'Comedy',
    'Animation',
    'Sci-Fi',
    'Crime',
    'Fantasy',
    'Documentary',
    'Family',
    'Film-Noir',
    'History',
    'Horror',
    'Musical',
    'Mystery',
    'Romance',
    'Sport',
    'Thriller',
    'War',
    'Western',
    'Biography'
]

print("Generating Best Movies Cards...")
f = open("best-template.html","r")
html_template = f.read()
f.close()

date = datetime.datetime.now()

card = '<figure class="post-card"><a href="https://greatermovies.com/movies/best-{#genre-mini}-movies-right-now"><img alt="Best {#genre-big} Movies Right Now" src="images/covers/{#genre-mini}-movies.jpg" /><h2>Best {#genre-big} Movies Right Now</h2><p>{#genre-upper} MOVIES</p></a></figure>'

cards = ""

for genre in genres:
    html = html_template.replace("{#genre-mini}", genre.lower())
    html = html.replace("{#genre-big}", genre)
    html = html.replace("{#date}", date.strftime("%Y-%m-%d"))
    html = html.replace("{#timestamp}", date.isoformat())

    with open("templates\\best-" + genre.lower() + "-movies-right-now.html", 'w') as f:
        f.write(html)

    card_html = card.replace("{#genre-mini}", genre.lower())
    card_html = card_html.replace("{#genre-big}", genre)
    card_html = card_html.replace("{#genre-upper}", genre.upper())

    cards += card_html

    print(genre + " -> DONE.")

with open("best-cards.html", 'w') as f:
    f.write(cards)

# most-popular-{#genre-mini}-movies

print("Generating Popular Movies Cards...")
f = open("popular-template.html","r")
html_template = f.read()
f.close()

date = datetime.datetime.now()

card = '<figure class="post-card"><a href="https://greatermovies.com/movies/most-popular-{#genre-mini}-movies"><img alt="Most Popular {#genre-big} Movies" src="https://greatermovies.com/images/covers/popular-{#genre-mini}.jpg" /><h2>Most Popular {#genre-big} Movies</h2><p>{#genre-upper} MOVIES</p></a></figure>'

cards = ""

for genre in genres:
    html = html_template.replace("{#genre-mini}", genre.lower())
    html = html.replace("{#genre-big}", genre)
    html = html.replace("{#date}", date.strftime("%Y-%m-%d"))
    html = html.replace("{#timestamp}", date.isoformat())

    with open("templates\\most-popular-" + genre.lower() + "-movies.html", 'w') as f:
        f.write(html)

    card_html = card.replace("{#genre-mini}", genre.lower())
    card_html = card_html.replace("{#genre-big}", genre)
    card_html = card_html.replace("{#genre-upper}", genre.upper())

    cards += card_html

    print(genre + " -> DONE.")

with open("popular-cards.html", 'w') as f:
    f.write(cards)
