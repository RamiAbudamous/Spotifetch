import spotifyFuncs
from time import sleep
import os

if __name__ == "__main__":
    #call api for info
    spotifyCreds = spotifyFuncs.getSpotifyCreds()

    while True:    
        current_track = spotifyFuncs.getSpotifyTrack(spotifyCreds)
        spotifyFuncs.getSongArt(current_track)
        sleep(1)
        
