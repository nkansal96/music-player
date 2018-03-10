import sys
import os
import signal
import pprint
import json
import urllib.request
import pygame
import pathlib
import threading

from pygame import mixer
from pathlib import Path

import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2

class SpotifyPlayer:
	def __init__(self, spotify_client_id, spotify_client_secret):

		self.currSongID = 1
		self.mp3Files = []
		self.mixer = mixer.init()

		self.tempDir = "mp3FilesTemp"
		if not os.path.exists(self.tempDir):
			os.makedirs(self.tempDir)

		credentials = oauth2.SpotifyClientCredentials(
			client_id=spotify_client_id,
			client_secret=spotify_client_secret)

		token = credentials.get_access_token()
		if not token:
			print("Could not get token")
			sys.exit()

		self.sp = spotipy.Spotify(auth=token)

	def __del__(self):
		for file in self.mp3Files:
			if (Path(file).is_file()):
				os.remove(file)
		os.rmdir(self.tempDir)

	def play_song(self, name, artist):
		searchQuery = name + " " + artist
		result = self.sp.search(searchQuery, limit=1, type="track", market="US")
		preview_url = result["tracks"]["items"][0]["preview_url"]
		if (preview_url == 'None'):
			print("Could not play song")
			return False

		# Downloads the MP3 file locally
		currFileName = "./" + self.tempDir + "/spotifyTemp" + str(self.currSongID) + ".mp3"
		urllib.request.urlretrieve(preview_url, currFileName)
		self.currSongID += 1
		self.mp3Files.append(currFileName)

		def playMP3(fileName):
			mixer.music.load(fileName)
			mixer.music.play(2)	# play() default arg is 1
			# For some reason, play() doens't work but does if it's argument is anything but 1
			# Currently plays for two iterations

		# Removes the MP3 file once song is done playing
		def checkPlayStatus(fileName):
			while pygame.mixer.music.get_busy():
				pass
			if (Path(fileName).is_file()):
				os.remove(fileName)

		threading.Thread(target=playMP3, args=(currFileName,)).start()
		threading.Thread(target=checkPlayStatus, args=(currFileName,)).start()

		return True
