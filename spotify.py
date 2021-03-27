import requests
import base64
import datetime
import webbrowser

CLIENT_ID = "2fa050e95ec846d0b60ecdfff3912f5d"
CLIENT_SECRET = "f693c82555044e3d8c07524f910382e5"


class SpotifyEndpoints:
    TOKEN = "https://accounts.spotify.com/api/token"
    SEARCH = "https://api.spotify.com/v1/search"
    ALBUM = "https://api.spotify.com/v1/artists/{artist_id}/albums"
    ALBUM_TRACKS = "https://api.spotify.com/v1/albums/{id}/tracks"


class Spotify:
    PLAYLIST_URL = "https://open.spotify.com/album/{album_single_id}"

    def __init__(self):
        self.access_token = None
        self.token_expire_time = -1

    def get_access_token(self):
        if self.access_token is not None and datetime.datetime.now().second < self.token_expire_time:
            return self.access_token
        client_credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode())
        r = requests.post(
            url=SpotifyEndpoints.TOKEN,
            data={"grant_type": "client_credentials"},
            headers={"Authorization": f"Basic {client_credentials.decode()}"}
        )
        valid_request = r.status_code in range(200, 299)
        if not valid_request:
            raise Exception(f"cannot get token. status code: {r.status_code}")
        token_response_data = r.json()
        self.access_token = token_response_data["access_token"]
        self.token_expire_time = token_response_data["expires_in"] + datetime.datetime.now().second
        return self.access_token

    def search_artist(self, query):
        r = requests.get(
            url=SpotifyEndpoints.SEARCH,
            headers={"Authorization": f"Bearer {self.get_access_token()}"},
            params={"q": query, "type": "artist"}
        )
        data = r.json()
        artist_id = data["artists"]["items"][0]["id"]
        artist_name = data["artists"]["items"][0]["name"]
        return artist_id, artist_name

    def get_artist_albums(self, artist_id):
        singles = []
        r = requests.get(
            url=SpotifyEndpoints.ALBUM.format(artist_id=artist_id),
            headers={"Authorization": f"Bearer {self.get_access_token()}"},
            params={"include_groups": "album,single"}
        )
        data = r.json()
        album_ids_names = {}
        albums = data["items"]
        for album in albums:
            if album["album_type"] == "album":
                if album["name"] not in album_ids_names.values():
                    album_ids_names[album["id"]] = album["name"]
                else:
                    continue
            else:
                singles.append(album["name"] + " " + album["release_date"].split("-")[0] + " " + album["id"])

        return album_ids_names, singles

    def get_album_tracks(self, album_id):
        r = requests.get(
            url=SpotifyEndpoints.ALBUM_TRACKS.format(id=album_id),
            headers={"Authorization": f"Bearer {self.get_access_token()}"},
            params={"limit": 50}
        )
        data = r.json()
        tracks = data["items"]
        return [track["name"] for track in tracks]

    @staticmethod
    def play_album_single(album_single_id):
        return webbrowser.open(url=Spotify.PLAYLIST_URL.format(album_single_id=album_single_id))
