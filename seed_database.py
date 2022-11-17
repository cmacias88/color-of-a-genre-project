"""Script to seed database."""

import os
import json
from random import choice, randint
from colorthief import ColorThief

import crud
import model
import server

os.system('dropdb visualplaylist')
os.system('createdb visualplaylist')

model.connect_to_db(server.app)
model.db.create_all()

for n in range(5):
    username = f'user{n}'
    password = 'test'

    user = crud.create_user(username, password)
    model.db.session.add(user)


genre_list = [
    "rock", "indie", "pop", "country", "rap", "hip hop", "jazz", 
    "classical", "metal", "alternative", "folk", "house", "punk"
    ]
    
for genre_name in genre_list:
    genre = crud.create_genre(genre_name)
    model.db.session.add(genre)


with open('data/playlists.json') as f:
    playlist_data = json.loads(f.read())


playlists_in_db = []
tracks_in_db = []

for playlist in playlist_data:

    playlist_uri = playlist["playliast_uri"]
    playlist_name = playlist["playlist_name"]
    for track in playlist["tracks"]:
        track_title, track_genre, track_artist, track_image = playlist["tracks"]
        color_thief = ColorThief(track_image)
        track_image_color = color_thief.get_color(quality=1)
        db_track = crud.create_track(track_title, track_genre, track_artist, track_image, track_image_color, playlist_uri)
        tracks_in_db.append(db_track)
    tracks = tracks_in_db 

    db_playlist = crud.create_playlist(playlist_uri, playlist_name, tracks)
    playlists_in_db.append(db_playlist)


model.db.session.add_all(playlists_in_db)
model.db.session.commit()