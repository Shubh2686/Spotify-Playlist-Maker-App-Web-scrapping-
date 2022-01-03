import requests
from bs4 import BeautifulSoup

date = input("which year do you want to travel to? Type the date in YYYY-MM-DD format: ")

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}")
contents = response.text
# print(response.text)
soup = BeautifulSoup(contents, "html.parser")
# print(soup.prettify())
songs = soup.find_all(name="h3",
                      class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 "
                             "lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 "
                             "u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 "
                             "u-max-width-230@tablet-only")
# print(songs)
songs_list = [song.text for song in songs]
i = 1
song_1 = soup.find_all(name='h3',
                       class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet "
                              "lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max "
                              "a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only "
                              "u-letter-spacing-0028@tablet")

songs_list.insert(0, song_1[0].text)
for song in songs_list:
    print(f"({i}){song}")
    i += 1

import spotipy
from spotipy.oauth2 import SpotifyOAuth

Domain = "http://example.com/?code=AQCr2DjH4LIXQnekFx4DVBI9a03tMBRL" \
         "-Rgr1uuuqrf6Yoe_dz2nqV2V0eO1SF2MdM8zwJlzLL56O3vxbvRJVeCk2RGpc5fO" \
         "-DntnYLtSVPjQj646qTS8xqicNQ0ey2mCSPIs5c5ZrpkV1mwcVxZUWrw8rYeEb7j9Nw6e-3zRsiDBJA6WjLkdZoiseNVhu8 "

scope = "playlist-modify-private"

Client_ID = "46d5b5839e52452da4e4f3a7363c2bab"
Client_Secret = "dbb94b54b7da4f2fad4a54cc873d1bd6"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=Client_ID, client_secret=Client_Secret, scope=scope,
                                               redirect_uri='http://example.com'))
user_id = sp.current_user()["id"]
# print(user_id)
songs_uri = []
for song in songs_list:
    search = sp.search(
        q=f'track:{song} year:{date.split("-")[0]}',
        type="track")
    try:
        songs_uri.append(search["tracks"]["items"][0]["uri"])
    except IndexError:
        continue
    # pprint.pprint(search["tracks"]["items"][0]["uri"])
# print(songs_uri)

playlist = sp.user_playlist_create(user=user_id, name=f"{date}Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist['id'], items=songs_uri)
