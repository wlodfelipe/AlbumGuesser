import requests
import random
from cs50 import SQL
from dotenv import load_dotenv

REPEATED_ALBUMS = []

db = SQL("sqlite:///albums.db")

def configure():
    load_dotenv()

def get_album_info(api_key, artist, album):
    base_url = "https://ws.audioscrobbler.com/2.0/"
    method = "album.getinfo"
    format_type = "json"

    params = {
        "method": method,
        "api_key": api_key,
        "artist": artist,
        "album": album,
        "format": format_type,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "error" in data:
        print(f"Error: {data['message']}")
        return None
    else:
        return data["album"]

def album_info(id):
    import os

    albumInfo = db.execute('SELECT release_name, artist_name, release_date FROM albums WHERE position = ?', id)
    print(albumInfo)
    key = os.getenv('api_key')

    artist = albumInfo[0]["artist_name"]
    album = albumInfo[0]["release_name"]
    date = albumInfo[0]["release_date"]


    album_info = get_album_info(key, artist, album)

    if album_info:
        print("Album Information:")
        print(f"Title: {album_info['name']}")
        print(f"Artist: {album_info['artist']}")
        print(f"Image URL: {album_info['image'][-1]['#text']}")

        return {
            "position": id,
            "artist": album_info['artist'],
            "name": album_info['name'],
            "image": album_info['image'][-1]['#text'],
            "release_date": date
        }


def getRandomAlbum(limit):
    randomID = random.randint(1, limit)
    if randomID in REPEATED_ALBUMS:
        if len(REPEATED_ALBUMS) > limit-1:
            REPEATED_ALBUMS.clear()
        return getRandomAlbum(limit)

    REPEATED_ALBUMS.append(randomID)

    return randomID


# algorithm that makes the guessing more fair, not necesseraly needing to type all the letters correctly
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]




