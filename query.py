from spotify import *

query = input("Artist: ")
spotify = Spotify()
artist_id, artist_name = spotify.search_artist(query)
print(f"Retrieving songs for {artist_name}")
albums, singles = spotify.get_artist_albums(artist_id)
for album_id in albums:
    songs = spotify.get_album_tracks(album_id)
    print(albums[album_id] + ":")
    for song in songs:
        print("\t" + song)

if len(singles) != 0:
    print("Singles:")
    for song in singles:
        print(song)

print("""
------------------
Done :)
Source: Spotify
------------------
""")
user_request = input("Album or Singles? (type s or a)\n")
if user_request == "a":
    album_request = " ".join(input("What album to play? ").title().split())
    for album_id, album_name in albums.items():
        if album_request == album_name:
            album_request_id = album_id
            spotify.play_album_single(album_request_id)
elif user_request == "s":
    single_request = " ".join(input("What single to play? ").title().split())
    for song in singles:
        x = song.split()
        single_id = x[-1]
        str_song = " ".join(x[:-2])
        if single_request == str_song:
            spotify.play_album_single(single_id)