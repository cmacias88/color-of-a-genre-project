from model import db, User, Visualization, Playlist, PlaylistTrack, Genre, Track, TrackGenre, TrackVisualization, VisualizationData, connect_to_db


def create_user(username, password):
    """Create and return a new user."""

    return User(username=username, password=password)


def get_all_users():
    """Gives all users."""

    return User.query.all()


def create_playlist(playlist_url, playlist_name, user_id, tracks):
    """Create a playlist."""

    playlist_given = Playlist.query.filter(Playlist.playlist_url == playlist_url)

    if playlist_given == None:
        return Playlist(playlist_url=playlist_url, playlist_name=playlist_name, user_id=user_id, tracks=tracks)


def create_track(track_title, track_genre, playlist_id, track_artist, track_image, track_image_color):
    """Create a track."""

    if track_title in Track and track_artist in Track: 
        pass 
    else:
        return Track(track_title=track_title, 
                track_genre=track_genre,
                track_artist=track_artist, 
                track_image=track_image,
                track_image_color=track_image_color,
                playlist_id=playlist_id)


def update_playlist(track_id, playlist_id):
    """Update playlist with a track."""

    playlist = Playlist.query.filter(Playlist.playlist_id == playlist.id).first()

    if track_id not in playlist.tracks:
        return PlaylistTrack(playlist_id=playlist_id,
                            track_id=track_id)


def get_all_tracks(playlist_id):
    """Gives all tracks from a playlist."""

    p = Playlist.query.filter(Playlist.id == playlist_id)

    return p.tracks


def create_genre(genre_name):
    """Create a genre."""

    def find_genre(genre_name):
        if genre_name in db.session.query.filter(Genre.genre_name).all():
            genre_name = db.session.query.filter(Genre.genre_name) 
        return genre_name 

    if genre_name != find_genre(genre_name):
        return Genre(genre_name)


def get_all_genres():
    """Gives all genres."""

    return Genre.query.all()


def create_visualization_data(playlist_id, visualization_id, genre_percentages, most_common_color):
    """Create visualization data from a playlist."""

    return VisualizationData(
        playlist_id=playlist_id,
        visualization_id=visualization_id,
        genre_percentages=genre_percentages, 
        most_common_color=most_common_color 
    )


def create_visualization(user_id, playlist_id, visualization_data):
    """Create and return a new visualization."""

    return Visualization(
        user_id=user_id,
        playlist_id=playlist_id,
        visualization_data_=visualization_data
    )


def get_all_user_visualizations(user_id):
    """Gives all visualizations under a certain user."""

    return Visualization.query.filter(Visualization.user_id == user_id).all()


def get_visualization_by_playlist(playlist_id):
    """Gives visualization for a certain playlist."""

    return Visualization.query.filter(Visualization.playlist_id == playlist_id).first()


def get_visualization_data_for_visualization(visualization_id):
    """Gives visualization data for a certain visualization."""

    return VisualizationData.query.filter(VisualizationData.visualization_id == visualization_id).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

