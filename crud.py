from model import db, User, Visualization, Playlist, Genre, Track, TrackGenre, VisualizationData, connect_to_db


def create_user(username, password):
    """Create and return a new user."""

    return User(username=username, password=password)


def get_all_users():
    """Gives all users."""

    return User.query.all()


def create_playlist(url, playlist_name, user_id, tracks):
    """Create a playlist."""

    return Playlist(url=url, playlist_name=playlist_name, user_id=user_id, tracks=tracks)


def create_track(track_title, track_genre, playlist_id, track_artist, track_image, track_image_color):
    """Create a track."""

    return Track(track_title=track_title, 
                track_genre=track_genre,
                track_artist=track_artist, 
                track_image=track_image,
                track_image_color=track_image_color,
                playlist_id=playlist_id)


def create_genre(genre_name):
    """Create a genre."""

    return Genre(genre_name)


def create_visualization(user_id, playlist_id, visualization_data):
    """Create and return a new visualization."""

    return Visualization(
        user_id=user_id,
        playlist_id=playlist_id,
        visualization_data=visualization_data
    )


def get_all_user_visualizations(user_id):
    """Gives all visualizations under a certain user."""

    return Visualization.query.filter(Visualization.user_id == user_id).all()


def get_visualization_by_playlist(playlist_id):
    """Gives visualization for a certain playlist."""

    return Visualization.query.filter(Visualization.playlist_id == playlist_id).first()


def create_visualization_data(playlist_id, visualization_id, genre_percentages, most_common_color):
    """Create visualization data from a playlist."""

    return VisualizationData(
        playlist_id=playlist_id,
        visualization_id=visualization_id,
        genre_percentages=genre_percentages, 
        most_common_color=most_common_color 
    )


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

