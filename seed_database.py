"""Script to seed database."""

import os
import json
from random import choice, randint
import colorsys 
from colorthief import ColorThief

import crud
import model
import server

import os, urllib.request, colorsys

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


def hsv_conversion(rgb_tuple):
    """Converts rgb values into hsv format."""
    rgb_copy = rgb_tuple[0:]
    r, g, b = rgb_copy
    (r, g, b) = (r / 255, g / 255, b / 255)
    (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
    (h, s, v) = (int(h * 360), int(s * 100), int(v * 100))
    return (h, s, v)


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
        rgb_color = dominant_color_from_url(track_image)
        (h, s, v) = hsv_conversion(rgb_color)
        if (0 <= h < 12) or (339 <= h <= 359) and (s > 7) and (v > 56):
            track_image_color = 'red'
        elif (12 <= h <= 41) and (s > 81) and (v > 56):
            track_image_color = 'orange'
        elif (42 <= h <= 69) and (s > 7) and (v > 8):
            track_image_color = 'yellow'
        elif (70 <= h <= 166) and (s > 7) and (v > 8):
            track_image_color = 'green'
        elif (167 <= h <= 251) and (s > 7) and (v > 8):
            track_image_color = 'blue'
        elif (252 <= h <= 305) and (s > 7) and (v > 8):
            track_image_color = 'purple'
        elif (306 <= h <= 338) and (s > 7) and (v > 8):
            track_image_color = 'pink'
        elif (s < 16) and (20 < v > 92):
            track_image_color = 'grey'
        elif (s < 5) and (v < 20) or (v == 0):
            track_image_color = 'black'
        elif (s < 3) and (v > 92):
            track_image_color = 'white'
        elif (12 < h < 35) and (20 < s < 81) and  (20 < v < 56):
            track_image_color = 'brown'

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
        
        total_track_num = len(db_playlist.tracks)

        track_genre_info = {}

        for track in db_playlist.tracks:
            track_genre_name = track.genre
            print(track_genre_name)
        #     if not track_genre_info[track_genre_name]:
        #         track_genre_info[track_genre_name]['count'] = 1
        #         track_genre_info[track_genre_name]['colors'] = {}
        #     else: 
        #         track_genre_info[track_genre_name]['count'] += 1

        # for track in db_playlist.tracks:
        #     track_color = track.track_image_color
        #     for track_genre in track_genre_info: 
        #         if not track_genre['colors'][track_color]:
        #             track_genre['colors'][track_color] = 1
        #         else: 
        #             track_genre['colors'][track_color] += 1

        # print(track_genre_info)

        # for genre in track_genre_info: 
        #     genre_percentage = ((track_genre_info[genre])/total_track_num) * 100
        #     for color, color_total in genre['colors'].items():
        #         genre_most_common_color = ['', 0]
        #         if color_total > most_common_color[1]:
        #             most_common_color = [color, color_total]

        # visualization_data = crud.create_visualization_data(playlist_id)
        # model.db.session.add(visualization_data)
        # model.db.session.commit()

    

