from model import db, User, Visualization, Playlist, PlaylistTrack, Genre, Track, TrackGenre, TrackVisualization, VisualizationData, connect_to_db


def create_user(fname, lname, username, password):
    """Create and return a new user."""

    return User(fname=fname, lname=lname, username=username, password=password)


def get_all_users():
    """Gives all users."""

    return User.query.all()


def get_user_by_username(username, password):
    """Gives user via their username."""

    return User.query.filter(User.username == username and User.password == password).first()


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
        return Genre(genre_name=genre_name)
    return genre


def create_track_genre(genre_id, track_id):
    """Add track to a genre."""

    track_genre = TrackGenre.query.filter(TrackGenre.genre_id == genre_id, TrackGenre.track_id == track_id).first()

    if not track_genre:
        return TrackGenre(genre_id=genre_id,
                        track_id=track_id)
    return track_genre


def get_all_genres():
    """Gives all genres."""

    return Genre.query.all()


def create_visualization_data(playlist_uri):
    """Create visualization data from a playlist."""

    playlist = Playlist.query.filter(Playlist.playlist_uri == playlist_uri).first()

    tracks = playlist.tracks
    track_nums = len(tracks)

    track_genre_count = {}
    track_genre_color = {}

    for track in tracks:
        track_genre = track.genre.name
        if not track_genre in track_genre_count:
            track_genre_count[track_genre] = 1
        else: 
            track_genre_count[track_genre] += 1 

    for track in tracks:
        track_genre = track.genre.name
        track_genre_color = {}

        if not track_genre in track_genre_color:
            track_genre_color[track_genre] = {}

        track_image_color = track.track_image_color 

        if track_image_color == 'red':
            if not track_genre_color[track_genre]['red']:
                track_genre_color[track_genre]['red'] = 1
            else: 
                track_genre_color[track_genre]['red'] += 1
        elif track_image_color == 'orange':
            if not track_genre_color[track_genre]['orange']:
                track_genre_color[track_genre]['orange'] = 1
            else: 
                track_genre_color[track_genre]['orange'] += 1
        elif track_image_color == 'yellow':
            if not track_genre_color[track_genre]['yellow']:
                track_genre_color[track_genre]['yellow'] = 1
            else: 
                track_genre_color[track_genre]['yellow'] += 1
        elif track_image_color == 'green':
            if not track_genre_color[track_genre]['green']:
                track_genre_color[track_genre]['green'] = 1
            else: 
                track_genre_color[track_genre]['green'] += 1
        elif track_image_color == 'blue':
            if not track_genre_color[track_genre]['blue']:
                track_genre_color[track_genre]['blue'] = 1
            else: 
                track_genre_color[track_genre]['blue'] += 1
        elif track_image_color == 'purple':
            if not track_genre_color[track_genre]['purple']:
                track_genre_color[track_genre]['purple'] = 1
            else: 
                track_genre_color[track_genre]['purple'] += 1
        elif track_image_color == 'pink':
            if not track_genre_color[track_genre]['pink']:
                track_genre_color[track_genre]['pink'] = 1
            else: 
                track_genre_color[track_genre]['pink'] += 1
        elif track_image_color == 'grey':
            if not track_genre_color[track_genre]['grey']:
                track_genre_color[track_genre]['grey'] = 1
            else: 
                track_genre_color[track_genre]['grey'] += 1 
        elif track_image_color == 'white':
            if not track_genre_color[track_genre]['white']:
                track_genre_color[track_genre]['white'] = 1
            else: 
                track_genre_color[track_genre]['white'] += 1
        elif track_image_color == 'black':
            if not track_genre_color[track_genre]['black']:
                track_genre_color[track_genre]['black'] = 1
            else: 
                track_genre_color[track_genre]['black'] += 1
        elif track_image_color == 'brown':
            if not track_genre_color[track_genre]['brown']:
                track_genre_color[track_genre]['brown'] = 1
            else: 
                track_genre_color[track_genre]['brown'] += 1

    # for value in track_genre_color[track_genre].values():
    #     genre_most_common_color = []


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


# def get_visualization_data_for_visualization(visualization_id):
#     """Gives visualization data for a certain visualization."""

#     return VisualizationData.query.filter(VisualizationData.visualization_id == visualization_id).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)

