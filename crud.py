from model import db, User, Visualization, Playlist, PlaylistTrack, Genre, Track, TrackGenre, TrackVisualization, VisualizationData, connect_to_db


def create_user(username, password):
    """Create and return a new user."""

    return User(username=username, password=password)


def get_all_users():
    """Gives all users."""

    return User.query.all()


def create_playlist(playlist_uri, playlist_name, tracks):
    """Create a playlist."""

    playlist_given = Playlist.query.filter(Playlist.playlist_uri == playlist_uri)

    if playlist_given == None:
        return Playlist(playlist_url=playlist_uri, playlist_name=playlist_name, tracks=tracks)


def update_playlist(track_id, playlist_uri):
    """Update playlist with a track."""

    playlist = Playlist.query.filter(Playlist.playlist_uri == playlist_uri).first()

    if track_id not in playlist.tracks:
        return PlaylistTrack(playlist_id=playlist.playlist_id,
                            track_id=track_id)


def create_track(track_title, track_genre, track_artist, track_image, track_image_color, playlist_uri,):
    """Create a track."""

    if track_title in Track and track_artist in Track: 
        pass 
    else:
        return Track(track_title=track_title, 
                track_genre=track_genre,
                track_artist=track_artist, 
                track_image=track_image,
                track_image_color=track_image_color,
                playlist_uri=playlist_uri)


def get_all_tracks(playlist_id):
    """Gives all tracks from a playlist."""

    playlist = Playlist.query.filter(Playlist.playlist_id == playlist_id)

    return playlist.tracks


def create_track_genre(track_id):
    """Gives track a genre."""

    track = Track.query.filter(Track.track_id == track_id)


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


def create_visualization_data(playlist_uri):
    """Create visualization data from a playlist."""

    playlist = Playlist.query.filter(Playlist.playlist_uri == playlist_uri).first()

    tracks = playlist.tracks
    track_nums = len(tracks)

    track_genre_count = {}

    for track in tracks:
        track_genre = track.trackgenre_id 
        if not track_genre:
            track_genre_count[track_genre] = 1
        else: 
            track_genre_count[track_genre] += 1 

    genre_percentages = []

    for genre_name, genre_tally in track_genre_count.items():
        genre_percentages.append({genre_name: (genre_tally/track_nums)})

    for track in tracks:
        track.

    return VisualizationData(
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

