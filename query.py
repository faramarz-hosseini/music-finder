import webbrowser
from spotify import *

query = input("Artist: ")
spotify_token = SpotifyToken()


class DataParse:
    def __init__(self):
        self.song_number = 1
        self.songs = {}
        self.singles = {}
        self.singles_number = 0

    @staticmethod
    def search_api_parse():
        response_from_search_api = SpotifyAPI.search_artist(query, spotify_token.get_access_token())
        artist_id = response_from_search_api["artists"]["items"][0]["id"]
        artist_name = response_from_search_api["artists"]["items"][0]["name"]
        return artist_id, artist_name

    def parse_album_api(self):
        response_from_album_api = SpotifyAPI.get_artist_albums(self.search_api_parse()[0], spotify_token.get_access_token())
        albums_data = response_from_album_api["items"]
        albums = {}
        singles = {}
        for album in albums_data:
            if album["album_type"] == "album":
                albums[album["id"]] = album["name"]
            elif album["album_type"] == "single":
                singles[album["external_urls"]["spotify"]] = {"name": album["name"], "id": album["id"]}
        return albums, singles

    @staticmethod
    def parse_album_tracks_api(album_id):
        response_from_album_tracks_api = SpotifyAPI.get_album_tracks(album_id, spotify_token.get_access_token())
        songs_data = response_from_album_tracks_api["items"]
        for song in songs_data:
            data_parse_obj.songs[song["id"]] = {
                "name": song["name"],
                "spotify": song["external_urls"]["spotify"],
                "song_number": data_parse_obj.song_number
            }
            data_parse_obj.song_number += 1
        return data_parse_obj.songs


def album_data_printer():
    print(f"Retrieving songs for {data_parse_obj.search_api_parse()[1]}...")
    for album_id, album_name in data_parse_obj.parse_album_api()[0].items():
        print(f"{album_name}:")
        for song in data_parse_obj.parse_album_tracks_api(album_id).values():
            print(f"\t -{song['name']} ({song['song_number']})")


def singles_data_printer():
    if len(data_parse_obj.parse_album_api()[1]) != 0:
        print("Singles:")
    for single_link, single_info in data_parse_obj.parse_album_api()[1].items():
        data_parse_obj.singles[single_info["id"]] = single_info["name"]
        data_parse_obj.songs[single_info['id']] = {
                "name": single_info["name"],
                "spotify": single_link,
                "song_number": data_parse_obj.song_number
            }
        print(f"\t -{single_info['name']} ({data_parse_obj.song_number})")
        data_parse_obj.song_number += 1


def prepare_song_links():
    song_number_link = {}
    for song_info in data_parse_obj.songs.values():
        song_number_link[song_info["song_number"]] = song_info["spotify"]
    return song_number_link


def play_track_album(song_link):
    try:
        user_search_single = int(input("Number of the song: "))
        webbrowser.open(url=song_link.get(user_search_single))
    except:
        print("Invalid number. Please try again.")


data_parse_obj = DataParse()
album_data_printer()
singles_data_printer()
prepare_song_links()
play_track_album(prepare_song_links())