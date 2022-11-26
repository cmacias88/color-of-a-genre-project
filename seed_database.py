"""Script to seed database."""

import os
import json
from random import choice, randint
import colorsys 
from colorthief import ColorThief

import crud
import model
import server

import os, urllib.request

os.system('dropdb visualplaylist')
os.system('createdb visualplaylist')

model.connect_to_db(server.app)
model.db.create_all()

def dominant_color_from_url(url,tmp_file='tmp.jpg'):
    '''Downloads the image file and analyzes the dominant color'''
    urllib.request.urlretrieve(url, tmp_file)
    color_thief = ColorThief(tmp_file)
    dominant_color = color_thief.get_color(quality=1)
    os.remove(tmp_file)
    return dominant_color

for n in range(5):
    fname = f'First{n}'
    lname = f'Last{n}'
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
    db_playlist = crud.create_playlist(playlist_uri, playlist_name)
    model.db.session.add(db_playlist)
    model.db.session.commit()
    playlist_id = db_playlist.playlist_id
    for track in playlist["tracks"]:
        track_title = track["track_title"]
        track_genre = track["track_genre"]
        track_artist =track["track_artist"] 
        track_image = track["track_image"]
        track_image_color = dominant_color_from_url(track_image)

        db_track = crud.create_track(track_title, track_artist, track_image, track_image_color)
        model.db.session.add(db_track)
        model.db.session.commit()

        playlist_track = crud.add_track_to_playlist(db_track.track_id, playlist_id)
        model.db.session.add(playlist_track)
        model.db.session.commit()

        genre = crud.create_genre(track_genre)
        model.db.session.add(genre)
        model.db.session.commit()

        track_genre = crud.create_track_genre(genre.genre_id, db_track.track_id)
        model.db.session.add(track_genre)
        model.db.session.commit()
        

    

