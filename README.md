# Music Player

A voice-enabled IoT music player. It currently supports using the following voice commands, with more planned for the future:

- Play a particular song
- Play songs by an artist
- Play songs from a playlist
- Play the next song
- Change the volume
- Pause
- Resume

It uses the [Aurora API](http://auroraapi.com) to understand voice commands and the [Spotify Web API](https://developer.spotify.com/web-api/) to query songs, artists, and playlists. Note that this version only plays 30-second preview clips for select songs since that is all that we can access using the Spotify Web API. A list of songs that we've identified as playable can be found in [songs.txt](https://github.com/nkansal96/music-player/blob/master/songs.txt) (although by no means are these the only ones!)

## Prerequesites

1. Create an account with [Aurora](http://dashboard.auroraapi.com).
  - Create an application and note down the **Application ID** and the **Application Token**.
2. Create a [Spotify Developer Account](https://developer.spotify.com/my-applications/)
  - Create an application and note its **Spotify client ID** and **Spotify client secret**.
3. Install the Aurora dependencies. Follow the directions under the **Installation** section of the [Aurora Python SDK](https://github.com/auroraapi/aurora-python).
4. This application was developed with **Python 3.5**, so that is the version of Python we recommend. We also recommend using a virtual environment. Clone the code and run `pip install -r requirements.txt`.

## Running the Application

The music player client is fully configurable using command line arguments:

```bash
$ python3 main.py -h
usage: main.py [-h] --app_id APP_ID --app_token APP_TOKEN
               [--device_id DEVICE_ID] --spotify_client_id SPOTIFY_CLIENT_ID
               --spotify_client_secret SPOTIFY_CLIENT_SECRET
               [--trigger_word TRIGGER_WORD] [--silence_len SILENCE_LEN]

optional arguments:
  -h, --help            show this help message and exit
  --app_id APP_ID       the Aurora app ID
  --app_token APP_TOKEN
                        the Aurora app token
  --device_id DEVICE_ID
                        the unique ID for this device
  --spotify_client_id SPOTIFY_CLIENT_ID
                        The Spotify client ID
  --spotify_client_secret SPOTIFY_CLIENT_SECRET
                        The Spotify client secret
  --trigger_word TRIGGER_WORD
                        the trigger word for listen for before detecting
                        commands
  --silence_len SILENCE_LEN
                        the amount of silence (seconds) to tolerate before
                        querying the Aurora API service
```

Assuming you have the following information:
- Aurora app ID: `AURORA_APP`
- Aurora app token: `AURORA_TOKEN`
- Spotify client ID: `SPOTIFY_CLIENT_ID`
- Spotify client token: `SPOTIFY_CLIENT_TOKEN`

You can run the application like so:

```bash
$ python3 main.py --app_id AURORA_APP \
                  --app_token AURORA_TOKEN \
                  --spotify_client_id SPOTIFY_CLIENT_ID \
                  --spotify_client_token SPOTIFY_CLIENT_TOKEN
Ready...
```

The default trigger word before the player accepts commands is `box`, although this can be changed with the `--trigger_word NEW_WORD` flag.

## Limitations

We haven't actually tested this on a Raspberry Pi, but we hypothesize that the player will not be able to differentiate commands from playing music. This is both a hardware and software limitation which we intent to overcome partially though software. Stay tuned!