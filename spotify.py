import requests
import base64
import datetime
import webbrowser

CLIENT_ID = "2fa050e95ec846d0b60ecdfff3912f5d"
CLIENT_SECRET = "d33fe5c4675849db940d6bcb2130925f"

http_proxy = "http://fodev.org:8118"
https_proxy = "http://fodev.org:8118"

proxyDict = {
              "http": http_proxy,
              "https": https_proxy,
            }


class SpotifyEndpoints:
    TOKEN = "https://accounts.spotify.com/api/token"
    SEARCH = "https://api.spotify.com/v1/search"
    ALBUM = "https://api.spotify.com/v1/artists/{artist_id}/albums"
    ALBUM_TRACKS = "https://api.spotify.com/v1/albums/{id}/tracks"
    PLAY_ALBUM_URL = "https://open.spotify.com/album/{album_id}"
    PLAY_SINGLE_URL = "https://open.spotify.com/track/{single_id}"


class Spotify:

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
            headers={"Authorization": f"Basic {client_credentials.decode()}"},
            proxies=proxyDict
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
            params={"q": query, "type": "artist"},
            proxies=proxyDict
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
            params={"include_groups": "album,single"},
            proxies=proxyDict
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
                singles.append(album["name"] + " " + album["release_date"].split("-")[0])

        return album_ids_names, singles

    def get_album_tracks(self, album_id):
        r = requests.get(
            url=SpotifyEndpoints.ALBUM_TRACKS.format(id=album_id),
            headers={"Authorization": f"Bearer {self.get_access_token()}"},
            params={"limit": 50},
            proxies=proxyDict
        )
        data = r.json()
        tracks = data["items"]
        track_count = 1
        track_ids = {}
        for track in tracks:
            track_ids[track_count] = track["external_urls"]["spotify"]
            track_count += 1
        return tracks

    @staticmethod
    def play_album(album_id):
        return webbrowser.open(url=SpotifyEndpoints.PLAY_ALBUM_URL.format(album_id=album_id))

    @staticmethod
    def play_single(single_id):
        return webbrowser.open(url=SpotifyEndpoints.PLAY_SINGLE_URL.format(single_id=single_id))
