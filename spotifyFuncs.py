import config
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import urllib.request
from PIL import Image

def getSpotifyCreds():
    client_path_dir = f"{config.LOCATION}/data/client.txt"
    client_path = os.path.expanduser(client_path_dir)
    with open(client_path, 'r') as client_file:
        clients = client_file.readlines()
        clientID = clients[0].strip()
        clientSec = clients[1].strip()
        redirectUri = clients[2].strip()
        username = clients[3].strip()

    #only need the first
    scope = 'user-read-playback-state user-read-currently-playing'
    # scope = 'user-modify-playback-state'
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

        neofetch_path = os.path.expanduser(config.PATH)
        urllib.request.urlretrieve(art, f"{neofetch_path}/spotifyImage.png")

        progress = int(current_track["progress_ms"]/1000)
        duration = int(song["duration_ms"]/1000)
        remaining = int(duration-progress)
        progress_bar = calcProgressBar(progress, duration)

        width = config.WIDTH
        songInfo = f"{progress_bar}  (-{remaining//60}:{str(remaining%60).zfill(2)}) {songTitle} - {artistList}\n"
        if len(songInfo)>(3*width): #only keep 2 lines of characters
            songInfo = songInfo[:(3*width)]

        if len(songInfo)>(2*width):
            before = songInfo[:(2*width)]
            after = songInfo[(2*width):]
            songString = before + (" " * width) + after
        else:
            songString = songInfo + "\n"

        file_path = f"{neofetch_path}/spotifySong.txt"
        with open(file_path, 'w') as file:
            file.write(songString)
