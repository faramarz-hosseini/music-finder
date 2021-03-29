import datetime

import requests
import base64

CLIENT_ID = "2fa050e95ec846d0b60ecdfff3912f5d"
CLIENT_SECRET = "d33fe5c4675849db940d6bcb2130925f"

proxies = {
    "http": "http://fodev.org:8118",
    "https": "http://fodev.org:8118",
}


class SpotifyAPI:
    ENDPOINTS = {
        "TOKEN": "https://accounts.spotify.com/api/token",
        "SEARCH": "https://api.spotify.com/v1/search",
        "ALBUM": "https://api.spotify.com/v1/artists/{artist_id}/albums",
        "ALBUM_TRACKS": "https://api.spotify.com/v1/albums/{id}/tracks",
    }

    @staticmethod
    def get_token():
        client_credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode())
        r = requests.post(
            url=SpotifyAPI.ENDPOINTS["TOKEN"],
            data={"grant_type": "client_credentials"},
            headers={"Authorization": f"Basic {client_credentials.decode()}"},
            proxies=proxies
        )
        valid_request = r.status_code in range(200, 299)
        if not valid_request:
            raise Exception(f"cannot get token. status code: {r.status_code}")
        return r.json()

    @staticmethod
    def search_artist(query, access_token):
        r = requests.get(
            url=SpotifyAPI.ENDPOINTS["SEARCH"],
            headers={"Authorization": f"Bearer {access_token}"},
            params={"q": query, "type": "artist"},
            proxies=proxies
        )
        return r.json()

    @staticmethod
    def get_artist_albums(artist_id, access_token):
        r = requests.get(
            url=SpotifyAPI.ENDPOINTS["ALBUM"].format(artist_id=artist_id),
            headers={"Authorization": f"Bearer {access_token}"},
            params={"include_groups": "album,single"},
            proxies=proxies
        )
        return r.json()

    @staticmethod
    def get_album_tracks(album_id, access_token):
        r = requests.get(
            url=SpotifyAPI.ENDPOINTS["ALBUM_TRACKS"].format(id=album_id),
            headers={"Authorization": f"Bearer {access_token}"},
            params={"limit": 50},
            proxies=proxies
        )
        return r.json()


class SpotifyToken:
    def __init__(self):
        self.access_token = None
        self.token_expiration_time = -1

    def get_access_token(self):
        if self.access_token is None or self.token_expiration_time < datetime.datetime.now().second:
            response = SpotifyAPI.get_token()
            self.access_token = response["access_token"]
            self.token_expiration_time = response["expires_in"] + datetime.datetime.now().second
        return self.access_token
