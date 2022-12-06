from flask import Flask, session, render_template, request, jsonify, flash, redirect
from model import db, connect_to_db
import crud
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from colorthief import ColorThief

import os, urllib.request, colorsys

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

app = Flask(__name__)
app.secret_key = 'dev'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/sign-up', methods=['POST'])
def make_user_account():
    """Creates a user."""

    fname = request.json.get('fname')
    lname = request.json.get('lname')
    username = request.json.get('username')
    password = request.json.get('password')

    if crud.get_user_by_username(username, password) == None:
        user_account = crud.create_user(fname=fname,
                                        lname=lname,
                                        username=username,
                                        password=password)
        db.session.add(user_account)
        db.session.commit()

        flash('Thank you for creating an account!')

        session['user'] = user_account

        return jsonify({'fname': fname,
                    'last_name': lname,
                    'username': username,
                    'password': password,
                    }),
    else:
        flash("There is already an account with the same username.")


@app.route('/api/log-in', methods=['POST'])
def check_user_login():
    """Sees if user is currently logged in."""

    username = request.json.get('username')
    password = request.json.get('password')

    user = crud.get_user_by_username(username, password)

    if user:
        session['user'] = user
        flash("You successfully logged in!")
        return jsonify(user)
    else: 
        flash("User does not exist. Please create an account or verify your information is correct.")
    return redirect('/')


@app.route('/api/genres')
def get_all_genres_json():
    """Return a JSON response with all genres."""

    genres = crud.get_all_genres()

    return jsonify({'genres': genres})


@app.route('/api/playlist-selection', methods=['POST'])
def make_playlist():
    """Creates a playlist."""

    playlist_link = request.json.get('playlist_link')

    user_playlist = sp.playlist(playlist_link)

    if user_playlist != None:
        playlist_name = user_playlist['name']
        playlist_uri : user_playlist['uri'] 
        db_playlist = crud.create_playlist(playlist_uri, playlist_name)

        db.session.add(db_playlist)
        db.session.commit()

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

        playlist_id = db_playlist.playlist_id

        tracks = sp.playlist_tracks(playlist_uri)
        for track in tracks:
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
            db.session.add(db_track)
            db.session.commit()

            playlist_track = crud.add_track_to_playlist(db_track.track_id, playlist_id)
            db.session.add(playlist_track)
            db.session.commit()

            genre = crud.create_genre(track_genre)
            db.session.add(genre)
            db.session.commit()

            track_genre = crud.create_track_genre(genre.genre_id, db_track.track_id)
            db.session.add(track_genre)
            db.session.commit()

        flash("Your playlist has been processed.")

        return jsonify({'playlist_uri': playlist_uri,
                        'playlist_name': playlist_name,
                        }), redirect('visualization-generator/<playlist_id>')


@app.route('api/visualization-generator/<playlist_id>', methods=['POST'])
def make_visualization_data(playlist_id):
    """Generates visualization from a playlist."""

    playlist = crud.get_playlist_by_id(playlist_id)

    total_track_num = len(playlist.tracks)

    track_genre_info = {}

    for track in playlist.tracks:
        track_genre_name = track.genre.name
        if not track_genre_info[track_genre_name]:
            track_genre_info[track_genre_name]['count'] = 1
            track_genre_info[track_genre_name]['colors'] = {}
        else: 
            track_genre_info[track_genre_name]['count'] += 1

    for track in playlist.tracks:
        track_color = track.track_image_color
        for track_genre in track_genre_info: 
            if not track_genre['colors'][track_color]:
                track_genre['colors'][track_color] = 1
            else: 
                track_genre['colors'][track_color] += 1
    
    for genre in track_genre_info: 
        genre_percentage = ((track_genre_info[genre])/total_track_num) * 100
        for color, color_total in genre['colors'].items():
            genre_most_common_color = ['', 0]
            if color_total > most_common_color[1]:
                most_common_color = [color, color_total]
        visualization_data = crud.create_visualization_data(genre_percentage, genre_most_common_color)
        db.session.add(visualization_data)
        db.session.commit()

    playlist_visualization_data = crud.get_visualization_data_for_visualization(playlist_id)

    return jsonify({'visualization_data': playlist_visualization_data})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")

