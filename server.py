from flask import Flask, session, render_template, request, jsonify, flash, redirect
from model import db, User, Visualization, Playlist, PlaylistTrack, Genre, Track, TrackGenre, TrackVisualization, VisualizationData, connect_to_db
import crud
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from colorthief import ColorThief

import os, urllib.request


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

    fname = request.post.json('fname')
    lname = request.post.json('lname')
    username = request.post.json('username')
    password = request.post.json('password')


    user_account = crud.create_user(fname=fname,
                                    lname=lname,
                                    username=username,
                                    password=password)

    db.session.add(user_account)
    db.session.commit()

    flash('Thank you for creating an account!')

    return jsonify({'fname': fname,
                    'last_name': lname,
                    'username': username,
                    'password': password,
                    })



@app.route('/api/log-in', methods=['POST'])
def check_user_login():
    """Sees if user is currently logged in."""

    username = request.get.json('username')
    password = request.get.json('password')

    user = crud.get_user_by_username(username, password)

    for users in crud.get_all_users(): 
        if user in users:
            session['user'] = user
            return jsonify(user)
        else: 
            flash("User does not exist. Please create an account or verify your information is correct.")
            return redirect('/log-in')


@app.route('/api/users')
def get_users_json():
    """Return a JSON response with all users."""

    users = crud.get_all_users()

    return jsonify({'users': users})


@app.route('/api/genres')
def get_all_genres_json():
    """Return a JSON response with all genres."""

    genres = crud.get_all_genres()

    return jsonify({'genres': genres})


@app.route('/api/playlist-selection', methods=['POST'])
def make_playlist():
    """Creates a playlist."""

    playlist_link = request.post.json('playlist_link')

    user_playlist = sp.playlist(playlist_link)

    playlist_name = user_playlist['name']
    playlist_uri : user_playlist['uri'] 
    tracks = []
        
    result = sp.playlist_tracks(playlist['playlist_uri'])
            
    for element in result['items']:
        track = element['track']
        artist_info = sp.artist(track['artists'][0]['href'])
        track_info = {'track_title': track['name'],
        'track_genre' : artist_info['genres'][0],
        'track_artist': track['artists'][0]['name'],
        'track_image': track['album']['images'][0]['url']}
        tracks.append(track_info)

    playlist = crud.create_playlist(playlist_uri=playlist_uri,
                                    playlist_name=playlist_name,
                                    )

    db.session.add(playlist)

    for track in playlist['tracks']:  
        track_title = track['name']
        track_genre = track['genre']
        track_artist = track['track_artist']
        track_image = track['track_image']
        def dominant_color_from_url(url,tmp_file='tmp.jpg'):
            '''Downloads ths image file and analyzes the dominant color'''
            urllib.urlretrieve(url, tmp_file)
            color_thief = ColorThief(tmp_file)
            dominant_color = color_thief.get_color(quality=1)
            os.remove(tmp_file)
            return dominant_color
        track_image_color = dominant_color_from_url(track_image)
        print(track_image_color)
        track = crud.create_track(track_title, track_genre, track_artist, track_image, track_image_color, playlist_uri)
        db.session.add(track)
    
    db.session.commit()

    flash('Your playlist has been processed.')

    return jsonify({'playlist_uri': playlist_uri,
                    'playlist_name': playlist_name,
                    'tracks': tracks
                    })


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")

