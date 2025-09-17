# Spotifetch

Like neofetch, but shows your currently playing song.

Requirements: 
- Fastfetch with chafa
- 'Spotipy' and 'Pillow' Python libraries
- zsh

## Setting Up:

### Setting up the Spotify end:
- Create an app on the [Spotify dashboard](https://developer.spotify.com/dashboard)
- Inside the app, note down your Client ID and Client secret. Set the Redirect URI field to `http://localhost:8888/callback`.
- Go to your [Spotify profile](https://www.spotify.com/us/account/profile/) and note down your username. Note that this is NOT the name you set for yourself, it should be a long string of random text.
- Once the app is done being created, create a `client.txt` file in the `data/` folder of the repo and put the following on individual lines:
  -  Client ID
  -  Client Secret
  -  Redirect URI (should be `http://localhost:8888/callback`)
  -  Username

### Setting up the system end:
- Edit the `config.py` file to set the directory and termianl width you want to use.
- Run the `main.py` file. It will ask you to sign into Spotify on your browser and cache your info.
- Check the directory you set to make sure everything is working. There should be 2 files, `spotifyImage.png` and `spotifySong.txt`.
- If everything looks good, go to your `.zshrc` and add the following snippet of code to the bottom of the file. Make sure to replace the `[PATH]` with the directory you set earlier.

```
# function that allows spotifetch to be called in the shell
spotifetch() {
    clear
    # use a separate config
    fastfetch --logo-recache --config ~/.config/fastfetch/spotifetch.jsonc    
    cat [PATH]/spotifySong.txt
}
```

- Copy your fastfetch config into a new file called `spotifetch.jsonc` in the `~/.config/fastfetch/` directory. 
- Edit the new config to change the chafa image to the `spotifyImage.png` path from earlier.
- Add `spotifetch` to the end of your `.zshrc`. If you already had `fastfetch` in there, remove it.
- Add the `main.py` file to your systemd so that it runs on boot. This is to constantly check for what song is being streamed.
- Reboot the system.
