from flask import Flask, session, render_template, request, jsonify, flash, redirect
from model import db, User, Visualization, Playlist, PlaylistTrack, Genre, Track, TrackGenre, TrackVisualization, VisualizationData, connect_to_db
import crud


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


@app.route("/api/genres")
def get_all_genres_json():
    """Return a JSON response with all genres."""

    genres = crud.get_all_genres()

    return jsonify({'genres': genres})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
