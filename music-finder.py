import requests
import base64
import datetime
user_search = input("Artist: ")
singles = []
songs = {}
client_id = "2fa050e95ec846d0b60ecdfff3912f5d"
client_secret = "f693c82555044e3d8c07524f910382e5"
token_url = "https://accounts.spotify.com/api/token"
method = "POST"
client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())
post_body = {
    "grant_type": "client_credentials"
}
post_headers = {
    "Authorization": f"Basic {client_creds_b64.decode()}"
}

r = requests.post(token_url, data=post_body, headers=post_headers)
valid_request = r.status_code in range(200, 299)
# print(r.json())
if valid_request:
    token_response_data = r.json()
    now = datetime.datetime.now()
    access_token = token_response_data["access_token"]
    expires_in = token_response_data["expires_in"]
    expires = now + datetime.timedelta(seconds=expires_in)
    did_expire = expires < now
    # print(access_token)

token_headers = {
    "Authorization": f"Bearer {access_token}"
}
search_endpoint = f"https://api.spotify.com/v1/search"
r2 = requests.get(search_endpoint, headers=token_headers, params={"q": user_search, "type": "artist"})
r2_data = r2.json()
artist_id = r2_data["artists"]["items"][0]["id"]
artist_name = r2_data["artists"]["items"][0]["name"]
# print(r2_data)
# print(artist_name + " ID:", artist_id)

albums_endpoint = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
r3 = requests.get(albums_endpoint, headers=token_headers, params={"include_groups": "album,single"})
r3_data = r3.json()
album_ids_names = {}
album_info = r3_data["items"]
for dic in album_info:
    if dic["album_type"] == "album":
        album_ids_names[dic["name"] + " " + dic["release_date"].split("-")[0]] = dic["id"]
    else:
        singles.append(dic["name"] + " " + dic["release_date"].split("-")[0])
# print(album_ids_names)


for album_name, id in album_ids_names.items():
    album_tracks_endpoint = f"https://api.spotify.com/v1/albums/{id}/tracks"
    r4 = requests.get(album_tracks_endpoint, headers=token_headers, params={"limit": 50})
    r4_data = r4.json()
    tracks_info = r4_data["items"]
    songs[f"{album_name}"] = []
    for dic in tracks_info:
        songs[f"{album_name}"].append(dic["name"])

for album_name, song_list in songs.items():
    print(album_name + ":")
    for song in song_list:
        print("    " + song)
    print("\n", end="")
if len(singles) != 0:
    print("Singles:")
    for song in list(dict.fromkeys(singles)):
        print("    " + song)

print("""
------------------
Done :)
Source: Spotify
------------------
""")


