import webbrowser
from spotify import *

query = input("Artist: ")


class SpotifyArtistManager:
    def __init__(self):
        self.token = SpotifyToken()
        self.song_num_to_url = {}

    def fetch_artist_info(self, artist_name):
        response_from_search_api = SpotifyAPI.search_artist(artist_name, self.token.get_access_token())
        try:
            artist_id = response_from_search_api["artists"]["items"][0]["id"]
            artist_name = response_from_search_api["artists"]["items"][0]["name"]
        except Exception:
            raise Exception("no artist was found with this name.")
        return artist_id, artist_name

    def fetch_artist_albums(self, artist_id):
        response_from_album_api = SpotifyAPI.get_artist_albums(
            artist_id=artist_id,
            access_token=self.token.get_access_token()
        )
        albums_data = response_from_album_api["items"]
        albums = {}
        singles = {}
        for album in albums_data:
            if album["album_type"] == "album":
                albums[album["id"]] = album["name"]
            elif album["album_type"] == "single":
                singles[album["id"]] = {"name": album["name"], "url": album["external_urls"]["spotify"]}
        return albums, singles

    def fetch_album_tracks(self, album_id):
        response_from_album_tracks_api = SpotifyAPI.get_album_tracks(album_id, self.token.get_access_token())
        songs_data = response_from_album_tracks_api["items"]
        songs = {song["id"]: {"name": song["name"], "spotify": song["external_urls"]["spotify"]} for song in songs_data}
        return songs

    def print_artist_songs(self, query):
        artist_id, artist_name = self.fetch_artist_info(query)
        print(f"Retrieving songs for {artist_name}...")
        albums, singles = self.fetch_artist_albums(artist_id)
        self.print_albums(albums)
        if len(singles):
            print("Singles:")
            self.print_singles(singles)

    def print_albums(self, albums):
        counter = 1
        for album_id, album_name in albums.items():
            print(f"{album_name}:")
            for song in self.fetch_album_tracks(album_id).values():
                print(f"\t - {song['name']} ({counter})")
                self.song_num_to_url[str(counter)] = song["spotify"]
                counter += 1

    def print_singles(self, singles):
        counter = 1
        for single_id, single_info in singles.items():
            print(f"\t - {single_info['name']} (s{counter})")
            self.song_num_to_url[f"s{counter}"] = single_info["url"]
            counter += 1


def open_track_url(songs_links):
    try:
        user_search_single = input("Number of the song: ")
        webbrowser.open(url=songs_links[user_search_single])
    except KeyError:
        print("Invalid number. Please try again.")


spotify_artist_manager = SpotifyArtistManager()
spotify_artist_manager.print_artist_songs(query)
while True:
    open_track_url(spotify_artist_manager.song_num_to_url)
