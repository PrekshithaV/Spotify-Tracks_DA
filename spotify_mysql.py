import re
from spotipy.oauth2 import (SpotifyClientCredentials)
import spotipy
import mysql.connector

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='547bb172cd8d4b7b9a46650fbc4938a1',
    client_secret='7852268affed4fba8787aa4e16a5f017'
))

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'spotify_db'
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

track_url = "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b"

track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

track = sp.track(track_id)

track_data = {
    'Track Name': track['name'],
    'Artist': track['artists'][0]['name'],
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)': track['duration_ms'] / 60000
}

insert_query = """
    INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
    VALUES (%s, %s, %s, %s, %s)
"""

cursor.execute(insert_query, (
    track_data['Track Name'],
    track_data['Artist'],
    track_data['Album'],
    track_data['Popularity'],
    track_data['Duration (minutes)']
))
connection.commit()

print(f"Track '{track_data['Track Name']}' by {track_data['Artist']} inserted into the database.")

cursor.close()
connection.close()

