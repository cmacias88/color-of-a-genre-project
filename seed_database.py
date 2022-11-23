"""Script to seed database."""

import os
import json
from random import choice, randint
import colorsys 
from colorthief import ColorThief

import crud
import model
import server

os.system('dropdb visualplaylist')
os.system('createdb visualplaylist')

model.connect_to_db(server.app)
model.db.create_all()


for n in range(5):
    fname = f'Test{n}'
    lname = f'Test{n}'
    username = f'user{n}'
    password = 'test'

    user = crud.create_user(fname, lname, username, password)
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

    playlist_uri = playlist["playlist_uri"]
    playlist_name = playlist["playlist_name"]
    for track in playlist["tracks"]:
        track_title = track["track_title"]
        track_genre = track["track_genre"]
        track_artist =track["track_artist"] 
        track_image = track["track_image"]
        print(track)
        print(track_image)
        # color_thief = ColorThief(track_image)
        # (r, g, b) = color_thief.get_color(quality=1)
        # track_image_color = [colorsys.rgb_to_hsv(r, g, b)]
        track_image_color = 'blue'
        db_track = crud.create_track(track_title, track_artist, track_image, track_image_color, playlist_uri)
        genre = crud.create_genre(track_genre)
        model.db.session.add(db_track)
        model.db.session.add(genre)
        model.db.session.commit()
        track_genre = crud.create_track_genre(genre.id, db_track.id)
        tracks_in_db.append(db_track)
    tracks = tracks_in_db 

    db_playlist = crud.create_playlist(playlist_uri, playlist_name, tracks)
    playlists_in_db.append(db_playlist)


model.db.session.add_all(playlists_in_db)
model.db.session.commit()