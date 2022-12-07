import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)


playlists = sp.user_playlists('31swwqnoren6yjiqvdc3vdkev4uy')

for playlist in playlists['items']:
    playlists['offset']
    print(f"playlist_uri: {playlist['uri']}") 
    print(f"playlist_name: {playlist['name']}")

    results = sp.playlist_tracks(playlist['uri'])

    for item in results['items']:
        track = item['track']
        print(f"track_title: {track['name']}")
        print(f"track_artist: {track['artists'][0]['name']}")
        track_artist_uri = track['artists'][0]['uri']
        track_artist = sp.artist(track_artist_uri)
        print(f"track_genre: {track_artist['genres'][0]}")
        print(f"track_image: {track['album']['images'][0]['url']}")
        print('***')
    
    print('---')
    print()
    print()




