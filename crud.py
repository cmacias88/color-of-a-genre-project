from model import db, User, Visualization, Playlist, PlaylistTrack, Genre, Track, TrackGenre, TrackVisualization, VisualizationData, PlaylistVisualizationData, connect_to_db


def create_user(fname, lname, username, password):
    """Create and return a new user."""

    return User(fname=fname, lname=lname, username=username, password=password)


def get_all_users():
    """Gives all users."""

    return User.query.all()


def get_user_by_username(username, password):
    """Gives user via their username."""

    return User.query.filter(User.username == username and User.password == password).first()


def get_playlist_by_id(playlist_id):
    """Gives playlist by id."""

    return Playlist.query.filter(Playlist.playlist_id == playlist_id).first()


def create_playlist(playlist_uri, playlist_name):
    """Create a playlist."""

    playlist_given = Playlist.query.filter(Playlist.playlist_uri == playlist_uri).first()

    if playlist_given == None:
        return Playlist(playlist_uri=playlist_uri, playlist_name=playlist_name)
    return playlist_given


def create_track(track_title, track_artist, track_image, track_image_color):
    """Create a track."""

    track = Track.query.filter(Track.track_title == track_title, Track.track_artist == track_artist).first()

    if track: 
        return track
    else:
        return Track(track_title=track_title, 
                track_artist=track_artist, 
                track_image=track_image,
                track_image_color=track_image_color
                )


def add_track_to_playlist(track_id, playlist_id):
    """Add track to a playlist."""

    playlist_track = PlaylistTrack.query.filter(PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.track_id == track_id).first()

    if not playlist_track:
        return PlaylistTrack(playlist_id=playlist_id,
                            track_id=track_id)
    return playlist_track


def get_all_tracks(playlist_id):
    """Gives all tracks from a playlist."""

    playlist = Playlist.query.filter(Playlist.playlist_id == playlist_id)

    return playlist.tracks


def create_genre(genre_name):
    """Create a genre."""

    genre = Genre.query.filter(Genre.genre_name == genre_name).first()

    if not genre: 
        return Genre(genre_name = genre_name)
    return genre

    # genre_list = Genre.query.filter(Genre.genre_name).all()

    # for genre in genre_list: 
    #     if genre_name in genre.genre_name: 
    #         return genre

    # return Genre(genre_name=genre_name)


def create_track_genre(genre_id, track_id):
    """Add track to a genre."""

    track_genre = TrackGenre.query.filter(TrackGenre.genre_id == genre_id, TrackGenre.track_id == track_id).first()

    if not track_genre:
        return TrackGenre(genre_id=genre_id,
                        track_id=track_id)
    return track_genre


def get_track_genre_name(track_id):
    """Add track to a genre."""

    track_match = TrackGenre.query.filter(TrackGenre.track_id == track_id).first()

    genre_match = track_match.genre_id

    genre = Genre.query.filter(Genre.genre_id == genre_match).first()

    return genre.genre_name


def get_all_genres():
    """Gives all genres."""

    genre_pool = Genre.query.all()

    return [genre.to_json() for genre in genre_pool]


def create_visualization_data(genre_percentage, genre_most_common_color):
    """Create visualization data from a playlist."""

    return VisualizationData(genre_percentage=genre_percentage,
                            genre_most_common_color=genre_most_common_color)
                            

def get_visualization_data_for_visualization(playlist_id):
    """Gives visualization data for a certain visualization."""

    all_data = PlaylistVisualizationData.query.filter(PlaylistVisualizationData.playlist_id == playlist_id).all()

    return [data.to_json() for data in all_data]


    # Need one visualization for the VisualizationData  
    # find library for sorting colors 

    # return VisualizationData(
    #     genre_percentage=genre_percentage, 
    #     genre_most_common_color=genre_most_common_color 
    # )


# def create_visualization(user_id, playlist_id, visualization_data):
#     """Create and return a new visualization."""

#     return Visualization(
#         user_id=user_id,
#         playlist_id=playlist_id,
#         visualization_data_=visualization_data
#     )


# def get_all_user_visualizations(user_id):
#     """Gives all visualizations under a certain user."""

#     return Visualization.query.filter(Visualization.user_id == user_id).all()


# def get_visualization_by_playlist(playlist_id):
#     """Gives visualization for a certain playlist."""

#     return Visualization.query.filter(Visualization.playlist_id == playlist_id).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

