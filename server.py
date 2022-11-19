from flask import Flask, jsonify, render_template
from model import db, User, Visualization, Playlist, PlaylistTrack, Genre, Track, TrackGenre, TrackVisualization, VisualizationData, connect_to_db
import crud


app = Flask(__name__)
app.secret_key = 'dev'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/users')
def get_users_json():
    """ Return a JSON response with all users. """

    users = crud.get_all_users()

    return jsonify({'users': users})


@app.route("/api/genres")
def get_all_genres_json():
    """ Return a JSON response with all genres. """

    genres = crud.get_all_genres()

    return jsonify({'genres': genres})



