import sys
import os
import signal
import pprint
import json
import urllib.request
import pygame
import pathlib
# import mplayer
# import vlc

from pygame import mixer
from pathlib import Path

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

import settings

# if len(sys.argv) > 1:
#   username = sys.argv[1]
# else:
#   print("Usage: %s username" % (sys.argv[0],))
#   sys.exit()

# Old Credentials
# scope = ''
# token = util.prompt_for_user_token(
# 	settings.NATHAN_USERNAME,
# 	scope,
# 	client_id=settings.SPOTIPY_CLIENT_ID,
# 	client_secret=settings.SPOTIPY_CLIENT_SECRET,
# 	redirect_uri=settings.SPOTIPY_REDIRECT_URI
# )

def sig_handler(signal, frame):
	if (Path("./spotifyTemp.mp3").is_file()):
		os.remove("./spotifyTemp.mp3")
	sys.exit()

def main():
	signal.signal(signal.SIGINT, sig_handler)

	songRequest = input("Enter a song name: ")
	artistRequest = input("Enter the artist: ")
	searchQuery = songRequest + " " + artistRequest
	print("Attempting to play " + songRequest + " by " + artistRequest)

	credentials = oauth2.SpotifyClientCredentials(
		client_id=settings.SPOTIPY_CLIENT_ID,
		client_secret=settings.SPOTIPY_CLIENT_SECRET)

	token = credentials.get_access_token()

	if not token:
		print("Could not get token")
		sys.exit()

	sp = spotipy.Spotify(auth=token)
	# result = sp.search("Uptown Funk", limit=1, type="track", market="US")
	# pprint.pprint(result)
	result = sp.search(searchQuery, limit=1, type="track", market="US")
	preview_url = result["tracks"]["items"][0]["preview_url"]
	if (preview_url == 'None'):
		print("Could not play song")
		sys.exit()

	print(preview_url)

	# Download MP3
	urllib.request.urlretrieve(preview_url, "./spotifyTemp.mp3")

	# Pygame code
	mixer.init()
	mixer.music.load("./spotifyTemp.mp3")
	mixer.music.play(2)	# play() default arg is 1
	# For some reason, play() doens't work but does if it's argument is anything but 1

	while pygame.mixer.music.get_busy(): 
		pygame.time.Clock().tick(10)

	if (Path("./spotifyTemp.mp3").is_file()):
		os.remove("./spotifyTemp.mp3")

	# mplayer code
	# p = mplayer.Player()
	# p.loadfile('/Users/thenathanyang/Music/Set\ final\ cut.mp3')

	# VLC code
	# p = vlc.MediaPlayer(preview_url)
	# p = vlc.MediaPlayer('/Users/thenathanyang/Music')
	# p.play()
	# p.get_instance()


if __name__ == "__main__":
	main()
