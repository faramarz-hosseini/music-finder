import webbrowser
from spotify import *


query = input("Artist: ")
spotify_token = SpotifyToken()
response = SpotifyAPI.search_artist(query, spotify_token.get_access_token())
artist_id, artist_name = response["artists"]["items"][0]["id"], response["artists"]["items"][0]["name"]
print(f"Retrieving songs for {artist_name}")

response = SpotifyAPI.get_artist_albums(artist_id, spotify_token.get_access_token())
albums = response["items"]
song_number = 1
albums_number = 1
album_links = {}
song_links = {}

for album in albums:
    response = SpotifyAPI.get_album_tracks(album["id"], spotify_token.get_access_token())
    songs = response["items"]
    album_links[albums_number] = album["external_urls"]["spotify"]
    print(f"{albums_number}) {album['name']}:")
    albums_number += 1
    for song in songs:
        song_links[song_number] = song["external_urls"]["spotify"]
        print(f"\t{song_number}- {song['name']}")
        song_number += 1

print("""
------------------
Done :)
Source: Spotify
------------------
""")

user_request = input("Album or Singles? (type s or a)\n")
song_request_text = "Number of the song: "
album_request_text = "Number of the album: "
while True:
    if user_request == "a":
        wanted_album_num = int(input(album_request_text))
        if album_links.get(wanted_album_num) is not None:
            wanted_album_href = album_links[wanted_album_num]
            webbrowser.open(url=wanted_album_href)
            break
        else:
            album_request_text = "Album was not found, try again. Number of the song: "
            wanted_album_num = int(input(album_request_text))
            continue
    elif user_request == "s":
        wanted_song_num = int(input(song_request_text))
        if song_links.get(wanted_song_num) is not None:
            wanted_song_href = song_links[wanted_song_num]
            webbrowser.open(url=wanted_song_href)
            break
        else:
            song_request_text = "Song was not found, try again. Number of the song: "
            wanted_song_num = int(input(song_request_text))
            continue
    else:
        user_request = input("Please type a for albums or s for songs.\n")
        continue
