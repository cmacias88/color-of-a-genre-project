"""Models for Color Of A Genre API."""

from platform import release
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    spotify_id = db.Column(db.String, unique=True)

    playlists = db.relationship("Playlist", back_populates="user")
    visualizations = db.relationship("Visualization", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} user={self.fname} {self.lname} username={self.username}>"


class TrackVisualization(db.Model):
    """The track for a given visualization."""

    __tablename__ = "track_visualizations"

    trackvisualization_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    visualization_id = db.Column(db.Integer, db.ForeignKey('visualizations.visualization_id'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.track_id'), nullable=False)

    def __repr__(self):
        return f"<TrackVisualization id={self.trackvisualization_id} visualization={self.visualization_id} track={self.track_id}>"


class Visualization(db.Model):
    """A visualization attributed to a user."""

    __tablename__ = "visualizations"

    visualization_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image = db.Column(db.String, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'), nullable=False)
    
    user = db.relationship("User", back_populates="visualizations")
    playlist = db.relationship("Playlist", back_populates="visualization")

    visualization_data = db.relationship("VisualizationData", uselist=False, back_populates="visualization")

    tracks = db.relationship("Track", secondary="track_visualizations", back_populates="visualizations")

    def __repr__(self):
        return f"<Visualization visualization_id={self.visualization_id} playlist_id={self.playlist_id} user_id={self.user_id}>"


class Playlist(db.Model):
    """A playlist and its data."""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_uri = db.Column(db.String, nullable=False, unique=True)
    playlist_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship("User", back_populates="playlists")
    visualization = db.relationship("Visualization", back_populates="playlist")

    tracks = db.relationship("Track", secondary="playlist_tracks", back_populates="playlists")

    def __repr__(self):
        return f"<Playlist playlist_id={self.playlist_id} name={self.playlist_name} user_id={self.user_id}>"


class PlaylistTrack(db.Model):
    """The tracks belonging in a playlist."""

    __tablename__ = "playlist_tracks"

    playlisttrack_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.track_id'), nullable=False)

    def __repr__(self):
        return f"<PlaylistTrack id={self.playlisttrack_id} playlist={self.playlist} track={self.track}>"


class Genre(db.Model):
    """A genre."""

    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_name = db.Column(db.String, nullable=False)

    tracks = db.relationship("Track", secondary="track_genres", back_populates="genre")

    def __repr__(self):
        return f"<Genre id={self.genre_id} name={self.genre_name}>"


class Track(db.Model):
    """A single track."""

    __tablename__ = "tracks"

    track_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    track_artist = db.Column(db.String, nullable=False)
    track_title = db.Column(db.String, nullable=False)
    track_image = db.Column(db.String, nullable=False) 
    track_image_color = db.Column(db.String, nullable=False)

    genre = db.relationship("Genre", secondary="track_genres", back_populates="tracks")
    playlists = db.relationship("Playlist", secondary="playlist_tracks", back_populates="tracks")
    visualizations = db.relationship("Visualization", secondary="track_visualizations", back_populates="tracks")

    def __repr__(self):
        return f"<Track id={self.track_id} title={self.track_title} artist={self.track_artist}>"


class TrackGenre(db.Model):
    """The genre of a given track."""

    __tablename__ = "track_genres"

    trackgenre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.track_id'), nullable=False)

    def __repr__(self):
        return f"<TrackGenre id={self.trackgenre_id} genre={self.genre} track={self.track}>"


class VisualizationData(db.Model):
    """The data for a visualization."""

    __tablename__ = "visualization_data"

    visualizationdata_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    genre_percentage = db.Column(db.FLOAT, nullable=False)
    genre_most_common_color = db.Column(db.String, nullable=False)
    genre_id = db.column(db.Integer, db.ForeignKey('genres.genre_id'))
    visualization_id = db.Column(db.Integer, db.ForeignKey('visualizations.visualization_id'), nullable=False)

    visualization = db.relationship("Visualization", uselist=False, back_populates="visualization_data")

    def __repr__(self):
        return f"<Visualization Data id={self.visualizationdata_id} visualization_id={self.visualization_id}>"


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