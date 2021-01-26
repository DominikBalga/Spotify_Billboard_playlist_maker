import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Getting song names in the chosen dates
date = input("Enter a date for playlist in this format - yyyy-mm-dd : ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
songs_full = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_names = [song.getText() for song in songs_full]
print(song_names)

# Creating a playlist for the chosen date

year = date.split("-")[0]
client_id_spotify = os.environ.get("ClientID")
client_secret_spotify = os.environ.get("ClientSecret")
uri = os.environ.get("Spotipy_uri")
scope = "playlist-modify-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id_spotify, client_secret_spotify, cache_path=".cache", scope=scope,
                              redirect_uri=uri, show_dialog=True))
user_id = sp.current_user()["id"]
create_playlist = sp.user_playlist_create(user=user_id, name=f"Top100 date: {date}", public=False)
i_d = create_playlist["id"]
uris = []
for name in song_names:
    song = sp.search(q=f"track:{name} year:{year}", type="track", limit=1)
    try:
        uri = song["tracks"]["items"][-1]["uri"]
        uris.append(uri)
    except IndexError:
        print(f"{name} skipped - in chosen year doesnt exist")
sp.playlist_add_items(playlist_id=i_d, items=uris)
