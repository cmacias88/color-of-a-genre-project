"""Models for Color Of a Genre API."""

from platform import release
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    spotify_id = db.Column(db.String, unique=True)

    playlists = db.relationship("Playlist", back_populates="users")
    visualizations = db.relationship("Visualization", back_populates="users")

    def __repr__(self):
        return f"<User user_id={self.id} spotify_id={self.spotify_id}>"


class Visualization(db.Model):
    """A visualization attributed to a user."""

    __tablename__ = "visualizations"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    
    user = db.relationship("User", back_populates="visualizations")

    visualization_data = db.relationship("visualization_data", uselist=False, back_populates="visualization")

    def __repr__(self):
        return f"<Visualization visualization_id={self.id} playlist_id={self.playlist_id} user_id={self.user_id}>"


class Playlist(db.Model):
    """A playlist and its data."""

    __tablename__ = "playlists"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship("User", back_populates="playlists")

    def __repr__(self):
        return f"<Playlist playlist_id={self.id} name={self.name} user_id={self.user_id}>"


class Genre(db.Model):
    """A genre."""

    __tablename__ = "genres"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False)

    genres = db.relationship("Genre", secondary="track_genres", back_populates="track")

    def __repr__(self):
        return f"<Genre id={self.id} name={self.name}>"


class Track(db.Model):
    """A single track in a playlist."""

    __tablename__ = "tracks"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artist = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    genre_name = db.Column(db.String, db.ForeignKey('genres.id'), nullable=False)
    song_image = db.Column(db.String, nullable=False) 
    song_image_color = db.Column(db.String, nullable=False)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)

    tracks = db.relationship("Track", secondary="track_genres", back_populates="genre")

    def __repr__(self):
        return f"<Track id={self.id} title={self.title} artist={self.artist}>"


class TrackGenre(db.Model):
    """The genre of a given track."""

    __tablename__ = "track_genres"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre = db.Column(db.String, db.ForeignKey('genres.id'), nullable=False)
    track = db.Column(db.String, db.ForeignKey('tracks.id'), nullable=False)

    def __repr__(self):
        return f"<TrackGenre id={self.id} genre={self.genre} track={self.track}>"


class VisualizationData(db.Model):
    """The data for a visualization."""

    __tablename__ = "visualization-data"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_percentage = db.Column(db.FLOAT, nullable=False)
    color_percentage = db.Column(db.FLOAT, nullable=False)
    visualization_id = db.Column(db.String, db.ForeignKey('visualizations.id'), nullable=False)

    visualization = db.relationship("visualization", uselist=False, back_populates="visualization_data")

    def __repr__(self):
        return f"<Visualization Data id={self.id} visualization_id={self.visualization_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///visualplaylist", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)