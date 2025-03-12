import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

def create_playlist(songs, name):
    load_dotenv()

    USER_ID = os.getenv('USER_ID')
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SECRET = os.getenv("SECRET")
    redirect_uri = "http://localhost:8888/callback/"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public", redirect_uri=redirect_uri, client_id=SPOTIPY_CLIENT_ID, client_secret=SECRET, cache_path="token.txt"))

    spotify_uris = []
    for song, artist in songs.values():
        result = sp.search(q=f"track:{song + " " + artist}",type="track")
        try:
            song_uri = result['tracks']['items'][0]['uri']
            spotify_uris.append(song_uri[14:])
        except:
            print(f"{song} not found.")
        
    my_playlist = sp.user_playlist_create(user=USER_ID, name=name, public=True, description="Copied playlist")
    spotify_track_ids = [spotify_uris[i:i + 100] for i in range(0, len(spotify_uris), 100)]

    for track_list in spotify_track_ids:
        sp.user_playlist_add_tracks(user=USER_ID, playlist_id=my_playlist['id'], tracks=track_list)
    
    return list(my_playlist['external_urls'].values())[0]