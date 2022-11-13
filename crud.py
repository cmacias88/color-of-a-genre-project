from model import db, User, Visualization, Playlist, Genre, Track, TrackGenre, VisualizationData, connect_to_db


def create_user(username, password):
    """Create and return a new user."""

    return User(username=username, password=password)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

