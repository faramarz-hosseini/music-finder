# Song Finder
Given the name of an artist, the program fetches a complete list of their albums (with their
respective songs) and singles using a variety of Spotify APIs. After the retrieval process, the user is given
the choice to enter a song number, after which the program opens a new tab in their browser and plays
their song on Spotify.
## How to run it
Open terminal, change direction (cd) into the project directory and:
```python
python3 query.py 
```
### spotify.py
Contains the SpotifyAPI. The instance of this class handles all the data retrieval from the public Spotify APIs.<br>
All of the endpoints (each for different purposes) used are defined in a dictionary as an attribute of the SpotifyAPI class.
```python
class SpotifyAPI:
    ENDPOINTS = {
        "TOKEN": "https://accounts.spotify.com/api/token",
        "SEARCH": "https://api.spotify.com/v1/search",
        "ALBUM": "https://api.spotify.com/v1/artists/{artist_id}/albums",
        "ALBUM_TRACKS": "https://api.spotify.com/v1/albums/{id}/tracks",
    }
```
<br></br>
#### Method: get_token
Using the Token endpoint, this method generates the credentials needed to request data from other endpoints. The method cleverly catches bad request with feedback as to what went wrong:
```python
        valid_request = r.status_code in range(200, 299)
        if not valid_request:
            raise Exception(f"cannot get token. status code: {r.status_code}")
        return r.json()
```

#### Method: search_artist
Performing a GET request on the Search endpoint, the method retrieves data on a certain artist. The artist name is passed to the method as an argument (query). the GET request is performed with query as one of its parameters. The access token is generated and passed to this method using the get_token method.
```python
    def search_artist(query, access_token):
        r = requests.get(
            url=SpotifyAPI.ENDPOINTS["SEARCH"],
            headers={"Authorization": f"Bearer {access_token}"},
            params={"q": query, "type": "artist"},
            proxies=proxies
        )
        return r.json()
```

#### Method: get_artist_albums
With the artist ID retrieved from the Search endpoint (using the above function, search_artist), the method performs a GET request on the Album endpoint and retrieves a list of album IDs for the queried artist. 

#### Method: get_album_tracks
This method takes an album_id as one of its arguments and then, returns a complete list of information about the songs in the given album. The idea is to use this method for each and every album ID that an artist has, to gather information on all songs of an artist. This method performs a GET request on the Album Tracks endpoint to achieve its purpose.

<br></br>
### query.py
 
Contains the SpotifyArtistManager class. The user is prompted to enter an artist name when the file is run, after which the methods of this class use the methods above to fetch, parse, and show data to the user. There are three methods that are responsible for feting and parsing data. This is done step by step by these three methods.
<li>fetch_artist_info()</li>
<li>fetch_artist_albums</li>
<li>fetch_album_tracks</li>
<br></br>

The data acquired from these methods are then passed to three other methods which are responsible for showing the data to the user. The method names make it obvious to know what data they show to the user.
<li>print_artist_songs()</li>
<li>print_albums()</li>
<li>print_singles()</li>

<br></br>
#### Function: open_track_url
After the data is fetched, printed and shown to the user, this method takes input from user and based on it, opens and plays one of the songs in the browser (The songs have numbers which can be used with this method to point to a song.)
```python
def open_track_url(songs_links):
    try:
        user_search_single = input("Number of the song: ")
        webbrowser.open(url=songs_links[user_search_single])
    except KeyError:
        print("Invalid number. Please try again.")
```
