import spotipy
from spotipy.oauth2 import SpotifyOAuth
# import spotipy.util as util
import os

import urllib.request
from PIL import Image
IMAGE_SIZE = 160

def getSpotifyCreds():
    client_path = os.path.expanduser("~/Desktop/projects/spotify_neofetch/data/client.txt")
    with open(client_path, 'r') as client_file:
        clients = client_file.readlines()
        clientID = clients[0].strip()
        clientSec = clients[1].strip()
        redirectUri = clients[2].strip()
        username = clients[3].strip()

    #only need the first
    scope = 'user-read-playback-state user-read-currently-playing user-modify-playback-state'
    # scope = 'user-modify-playback-state'

    # token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSec, redirect_uri=redirectUri)
    # spotify = spotipy.Spotify(auth=token)
    spotifyCreds = spotipy.Spotify(auth_manager=SpotifyOAuth(username=username, scope=scope, client_id=clientID, client_secret=clientSec, redirect_uri=redirectUri))
    return spotifyCreds


def calcProgressBar(progress, duration, segments=36):
    percentage = progress/duration
    filledSegments = int(percentage*segments)
    bar = "█" * filledSegments + "-" * (segments-filledSegments)
    return f"[{bar}]"

def getSpotifyTrack(sp):
    return sp.current_user_playing_track()

def getSongArt(current_track):
    if current_track!=None:
        song = current_track["item"]
        art = song["album"]["images"][1]["url"]    
        songTitle = song["name"]

        artists = []
        for artist in song["artists"]:
            artists.append(artist["name"])

        artistList = ""
        if len(artists)==1:
            artistList = artists[0]
        elif len(artists)>1:
            for i in range(len(artists)-1):
                artistList += f"{artists[i]}, "
            artistList += f"{artists[len(artists)-1]}"

        neofetch_path = os.path.expanduser("~/Documents/neofetch/")
        urllib.request.urlretrieve(art, f"{neofetch_path}/spotifyImage.png")

        progress = int(current_track["progress_ms"]/1000)
        duration = int(song["duration_ms"]/1000)
        remaining = int(duration-progress)
        progress_bar = calcProgressBar(progress, duration)

        songInfo = f"{progress_bar}  (-{remaining//60}:{str(remaining%60).zfill(2)}) {songTitle} - {artistList}\n"
        if len(songInfo)>120: #only keep the first 120 characters
            songInfo = songInfo[:120]

        if len(songInfo)>80:
            before = songInfo[:80]
            after = songInfo[80:]
            songString = before + (" " * 40) + after
        else:
            songString = songInfo + "\n"

        file_path = f"{neofetch_path}/spotifySong.txt"
        with open(file_path, 'w') as file:
            file.write(songString)
