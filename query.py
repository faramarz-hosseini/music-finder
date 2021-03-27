from spotify import *

query = input("Artist: ")
spotify = Spotify()
artist_id, artist_name = spotify.search_artist(query)
print(f"Retrieving songs for {artist_name}")
albums, singles = spotify.get_artist_albums(artist_id)
song_number = 1
albums_number = 1
album_ids = {}
song_ids = {}
for album_id in albums:
    songs = spotify.get_album_tracks(album_id)
    album_ids[albums_number] = album_id
    print(str(albums_number) + ") " + albums[album_id] + ":")
    albums_number += 1
    for song in songs:
        song_ids[song_number] = song["id"]
        print("\t" + str(song_number) + " " + song["name"])
        song_number += 1

if len(singles) != 0:
    print("Singles:")
    for song in singles:
        print("\t" + str(song_number) + " " + song)

print("""
------------------
Done :)
Source: Spotify
------------------
""")
user_request = input("Album or Singles? (type s or a)\n")
song_request_text = "Number of the song: "
album_request_text = "Number of the album: "
query_run = True
while query_run:
    if user_request == "a":
        wanted_album_num = int(input(album_request_text))
        if wanted_album_num in album_ids.keys():
            wanted_album_id = album_ids[wanted_album_num]
            Spotify.play_album(wanted_album_id)
            query_run = False
        else:
            album_request_text = "Album was not found, try again. Number of the song: "
            wanted_album_num = int(input(album_request_text))
            continue
    elif user_request == "s":
        wanted_song_num = int(input(song_request_text))
        if wanted_song_num in song_ids.keys():
            wanted_song_id = song_ids[wanted_song_num]
            Spotify.play_single(wanted_song_id)
            query_run = False
        else:
            song_request_text = "Song was not found, try again. Number of the song: "
            wanted_song_num = int(input(song_request_text))
            continue
    else:
        user_request = input("Please type a for albums or s for songs.\n")
        continue

# if user_request == "a":
#     album_request = " ".join(input("What album to play? ").title().split())
#     for album_id, album_name in albums.items():
#         if album_request == album_name:
#             album_request_id = album_id
#             spotify.play_album_single(album_request_id)
# elif user_request == "s":
#     single_request = " ".join(input("What single to play? ").title().split())
#     for song in singles:
#         x = song.split()
#         single_id = x[-1]
#         str_song = " ".join(x[:-2])
#         if single_request == str_song:
#             spotify.play_album_single(single_id)